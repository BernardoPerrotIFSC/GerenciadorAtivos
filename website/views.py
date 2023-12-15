from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import json
from website import db
from .models import Acao, Crypto, CarteiraAcoes, CarteiraCripto, Conta, HistAcao, HistCripto, Usuario
from datetime import datetime
from sqlalchemy.sql import func
import yfinance as yf

views = Blueprint('views',__name__)

#HOME
@views.route('/')
@login_required
def home():
    ativo = yf.Ticker("USDBRL=X")
    cotacao_dol = round(ativo.history(period='1d')['Close'][0], 2)
    carteira_acoes = CarteiraAcoes.query.filter_by(usuario_id = current_user.id).first()
    carteira_criptos = CarteiraCripto.query.filter_by(usuario_id = current_user.id).first()
    total_acoes = round(carteira_acoes.valor_atual_total, 2)
    total_dividendos = round(carteira_acoes.total_dividendos, 2)
    total_cripto = round(carteira_criptos.valor_atual_total, 2)
    total_cripto_real = round(total_cripto * cotacao_dol, 2)
    total = round(total_acoes+total_cripto_real, 2)
    return render_template("home.html", usuario=current_user, total=total, total_cripto_real=total_cripto_real, total_acoes=total_acoes, total_dividendos=total_dividendos, total_cripto=total_cripto)

#CONTA
@views.route('/conta', methods=["GET","POST"])
@login_required
def conta():
    if request.method == "POST":
        conta = Conta.query.filter_by(usuario_id=current_user.id)
        valor_adicioando = float(request.form.get("insere_valor"))
        conta.saldo += valor_adicioando
        db.session.commit()
    return render_template("conta/conta.html", usuario=current_user)

#ADD CONTA
@views.route('/add-conta', methods=["GET","POST"])
@login_required
def add_conta():
    return render_template("conta/add_conta.html", usuario=current_user)

#HIST CONTA
@views.route('/hist-conta', methods=["GET","POST"])
@login_required
def hist_conta():
    return render_template("conta/hist_conta.html", usuario=current_user)

#TABELA AÇÃO
@views.route('/acoes', methods= ['GET','POST'])
@login_required
def acoes():
    return render_template('acao/acoes.html', usuario = current_user)

#CRIA AÇÃO
@views.route('/add-acao', methods= ['GET', 'POST'])
@login_required
def add_acao():
    try:
        if request.method == 'POST':
            codigo = request.form.get('ticker')
            preco_pago = float(request.form.get('preco_pago'))
            quantidade = int(request.form.get('quantidade'))
            data_compra_str = request.form.get('dataCompra')
            descricao = request.form.get('descricao')
            codigo = codigo.upper()
            link = "https://www.tradingview.com/symbols/BMFBOVESPA-"+codigo+"/"
            ticker = codigo+".SA"
            valor_pago = round(preco_pago*quantidade, 2)
            acao = yf.Ticker(ticker)
            preco_atual = round(acao.history(period='1d')['Close'][0], 2)
            valor_atual = round(preco_atual*quantidade, 2)
            lucro_prejuizo = round(valor_atual-valor_pago, 2)
            rentabilidade = round(lucro_prejuizo/valor_pago*100, 2)
            data_compra = datetime.strptime(data_compra_str, '%Y-%m-%d')
            if rentabilidade > 0:
                status = "lucro"
            elif rentabilidade == 0:
                status = "zero"
            else:
                status = "prejuizo"
            nova_acao = Acao(ticker = codigo, preco_pago = preco_pago, quantidade = quantidade, valor_pago = valor_pago, preco_atual = preco_atual, valor_atual= valor_atual,rentabilidade= rentabilidade, lucro_prejuizo=lucro_prejuizo, data_compra = data_compra, status = status, usuario_id = current_user.id, link=link)
            hist_acao = HistAcao(usuario_id = current_user.id, ticker=codigo, descricao=descricao, quantidade=quantidade, preco = preco_pago, valor = valor_pago, tipo = "compra", data = data_compra)
            db.session.add(hist_acao)
            db.session.add(nova_acao)
            db.session.commit()
            flash(f"{ticker} adicionada a carteira", category='success')
            return redirect(url_for('views.add-acao'))
    except:
        flash("Não foi possível!", category="error")
    return render_template('acao/add_acao.html', usuario=current_user)

#REMOVE AÇÃO
@views.route('/remove-Acao', methods = ['POST'])
@login_required
def remover_acao():
    data = json.loads(request.data)
    acao_id = data["acaoId"]
    acao = Acao.query.get(acao_id)
    if acao:
        if acao.usuario_id == current_user.id:
            db.session.delete(acao)
            db.session.commit()
            flash("Ação removida da carteira!", category='success')
    return jsonify({})

#VENDE ACAO
@views.route('/rm-acao', methods=['POST','GET'])
@login_required
def rm_acao():
    try:
        if request.method == 'POST':
            ticker = request.form.get('ticker_venda')
            preco = float(request.form.get('preco_venda'))
            quantidade = int(request.form.get('quantidade_venda'))
            descricao = request.form.get('descricao_venda')
            data_str = request.form.get('dataVenda')    
            codigo = ticker.upper()
            data_venda = datetime.strptime(data_str, '%Y-%m-%d')
            qry = Acao.query.filter_by(ticker=codigo).filter_by(quantidade=quantidade).filter_by(usuario_id=current_user.id).first()
            if qry:
                hist = HistAcao(usuario_id = current_user.id, ticker = codigo, descricao=descricao, preco= preco, quantidade=quantidade, valor = preco*quantidade, tipo="venda", data = data_venda)
                db.session.add(hist)
                db.session.delete(qry)
                db.session.commit()
                flash(f'{codigo} removida da carteira e adiconada ao histórico!', category="success")
            else: 
                flash("Ação ou quantidade não foram encontradas", category='error')
        
    except:
        flash('Não foi possível!', category='error')
    return render_template('acao/rm_acao.html', usuario= current_user)

#ATUALIZA AÇÃO
@views.route('/atualiza-Acoes', methods = ['POST', 'GET'])
@login_required
def atualiza_acao():
    current_time = datetime.now()
    try:
        acoes = Acao.query.all()
        for acao in acoes:
            if acao.usuario_id == current_user.id:
                ativo = yf.Ticker(acao.ticker+".SA")
                acao.preco_atual = round(ativo.history(period='1d')['Close'][0], 2)
                acao.valor_atual = round(acao.preco_atual*acao.quantidade, 2)
                acao.lucro_prejuizo = round(acao.valor_atual-acao.valor_pago, 2)
                acao.rentabilidade = round(acao.lucro_prejuizo/acao.valor_pago*100, 2)
                if acao.rentabilidade > 0:
                    acao.status = "lucro"
                elif acao.rentabilidade == 0:
                    acao.status = "zero"
                else:
                    acao.status = "prejuizo"
                db.session.commit()
        qry = db.session.query(func.sum(Acao.valor_pago).label("valor_pago"),
                            func.sum(Acao.valor_atual).label("preco_atual")).filter_by(usuario_id=current_user.id)
        valores = qry.first()
        carteira = CarteiraAcoes.query.filter_by(usuario_id=current_user.id).first()
        ValorPago = valores[0]
        ValorAtual = valores[1]
        carteira.valor_pago_total = round(ValorPago, 2)
        carteira.valor_atual_total = round(ValorAtual, 2)
        carteira.lucro_prejuizo = round(ValorAtual - ValorPago, 2)
        carteira.rentabilidade_total = round(carteira.lucro_prejuizo/ValorPago*100, 2)
        if carteira.rentabilidade_total > 0:
            carteira.status = "lucro"
        elif carteira.rentabilidade_total == 0:
            acao.status = "zero"
        else:
            carteira.status = "prejuizo"
        carteira.last_update = current_time
        db.session.commit()
        flash("Valores atualizados", category='success')
        return redirect(url_for('views.acoes'))
    except:
        flash("Não foi possível!", category="error")
        return redirect(url_for('views.acoes'))

@views.route('/atualiza-Dividendos', methods = ['POST', 'GET'])
@login_required
def atualiza_dividendos():
    try:
        acoes = Acao.query.all()
        for acao in acoes:
            if acao.usuario_id == current_user.id:
                ativo = yf.Ticker(acao.ticker+".SA")
                dividend_info = ativo.dividends
                acao.last_yield = round(dividend_info.iloc[-1],2)
                data_compra_str = acao.data_compra.strftime("%Y-%m-%d")
                filtered_dividends = dividend_info[dividend_info.index >= data_compra_str]
                total = 0
                count = -1
                for i in filtered_dividends:
                    dividend = dividend_info.iloc[count]
                    total = total + dividend
                    count = count -1
                acao.total_dividends = round(total * acao.quantidade, 2)
                retorno = round(total * acao.quantidade, 2)
                acao.yield_total = round((retorno/acao.valor_pago) * 100, 2)
                print(acao.yield_total)
                db.session.commit()
        qry = db.session.query(func.sum(Acao.total_dividends).label("total_dividends")).filter_by(usuario_id=current_user.id)
        valores = qry.first()
        carteira = CarteiraAcoes.query.filter_by(usuario_id=current_user.id).first()
        TotalDividendos = valores[0]
        carteira.total_dividendos = round(TotalDividendos, 2)
        db.session.commit()
        flash("Dividendos atualizados", category='success')
        return redirect(url_for('views.acoes'))
    except:
        flash("Não foi possível!", category="error")
        return redirect(url_for('views.acoes'))
#HIST_ACAO
@views.route("/hist-acao", methods=["GET","POST"])
@login_required
def hist_acao():
    return render_template("acao/hist_acao.html", usuario=current_user)

#CRYPTO
@views.route('/cryptos', methods = ['GET', 'POST'])
@login_required
def cryptos():
    return render_template("cripto/crypto.html", usuario = current_user)

#REMOVE CRYPTO
@views.route('/remove-Crypto', methods = ['POST'])
@login_required
def remover_crypto():
    data = json.loads(request.data)
    crypto_id = data["cryptoId"]
    crypto = Crypto.query.get(crypto_id)
    if crypto:
        if crypto.usuario_id == current_user.id:
            ticker_excluido = crypto.ticker
            db.session.delete(crypto)
            db.session.commit()
            flash(f"Crypto {ticker_excluido} removida da carteira!", category='success')
    return jsonify({})

#ATUALIZAR CRYPTOS
@views.route('/atualiza-Crypto', methods = ['POST', 'GET'])
@login_required
def atualiza_crypto():
    current_time = datetime.now()
    try:
        cryptos = Crypto.query.filter_by(usuario_id=current_user.id).all()
        for crypto in cryptos:
            if crypto.usuario_id == current_user.id:
                ativo = yf.Ticker(crypto.ticker+"-USD")
                crypto.preco_atual = round(ativo.history(period='1d')['Close'][0], 3)
                crypto.valor_atual = round(crypto.preco_atual*crypto.quantidade, 2)
                crypto.lucro_prejuizo = round(crypto.valor_atual-crypto.valor_pago, 2)
                crypto.rentabilidade = round(crypto.lucro_prejuizo/crypto.valor_pago*100, 2)
                if crypto.rentabilidade > 0:
                    crypto.status = "lucro"
                elif crypto.rentabilidade == 0:
                    crypto.status = "zero"
                else:
                    crypto.status = "prejuizo"
                db.session.commit()
        qry = db.session.query(func.sum(Crypto.valor_pago).label("valor_pago"),
                            func.sum(Crypto.valor_atual).label("preco_atual")).filter_by(usuario_id=current_user.id)
        valores = qry.first()
        carteira = CarteiraCripto.query.filter_by(usuario_id=current_user.id).first()
        ValorPago = valores[0]
        ValorAtual = valores[1]
        carteira.valor_pago_total = round(ValorPago, 2)
        carteira.valor_atual_total = round(ValorAtual, 2)
        carteira.lucro_prejuizo = round(ValorAtual - ValorPago, 2)
        carteira.rentabilidade_total = round(carteira.lucro_prejuizo/ValorPago*100, 2)
        if carteira.rentabilidade_total > 0:
            carteira.status = "lucro"
        elif carteira.rentabilidade_total == 0:
            carteira.status = "zero"
        else:
            carteira.status = "prejuizo"
        carteira.last_update = current_time
        db.session.commit()

        flash("Valores atualizados", category='success')
        return redirect(url_for('views.cryptos'))          
    except:
        flash("Não foi possível", category='error')
        return redirect(url_for('views.cryptos'))
    
#HIST CRIPTOS
@views.route('/hist-cripto', methods=['POST', 'GET'])
@login_required
def hist_cripto():
    return render_template("cripto/hist_cripto.html", usuario=current_user)

#CRIAR CRIPTO
@views.route('add-cripto', methods=['GET','POST'])
@login_required
def add_cripto():
    try:
        if request.method == "POST":
            codigo = request.form.get('ticker_crypto')
            preco_pago = float(request.form.get('preco_pago_crypto'))
            quantidade = float(request.form.get('quantidade_crypto'))
            descricao = request.form.get('descricao_crypto')
            data_compra_str = request.form.get('dataCompra_crypto')
            codigo = codigo.upper()
            link = "https://www.tradingview.com/symbols/"+codigo+"USDT/"
            ticker = codigo+"-USD"
            ativo = Crypto.query.filter_by(ticker=codigo).filter_by(usuario_id=current_user.id).first()
            data_compra = datetime.strptime(data_compra_str, '%Y-%m-%d')
            print(ativo)
            if ativo:
                valor_pago = round(preco_pago*quantidade, 2)
                ativo.quantidade = ativo.quantidade + quantidade
                ativo.preco_pago = round((ativo.valor_pago+valor_pago)/(ativo.quantidade), 3)
                ativo.valor_pago = round(ativo.valor_pago+valor_pago , 2)
                ativo.valor_atual = round(ativo.preco_atual*ativo.quantidade, 2)
                ativo.lucro_prejuizo = round(ativo.valor_atual - ativo.valor_pago, 2)
                ativo.rentabilidade = round(ativo.lucro_prejuizo/ativo.valor_pago*100, 2)
                if ativo.rentabilidade > 0:
                    ativo.status = "lucro"
                elif ativo.rentabilidade == 0:
                    ativo.status = "zero"
                else:
                    ativo.status = "prejuizo"
                db.session.commit()
                flash(f"Mais {quantidade} criptos foram adicionadas a {ativo.ticker}")
                hist = HistCripto(usuario_id=current_user.id, ticker = codigo, descricao=descricao, preco = preco_pago, quantidade=quantidade, valor=preco_pago*quantidade, tipo="compra", data=data_compra)
                db.session.add(hist)
                db.session.commit()
            else:
                valor_pago = round(preco_pago*quantidade, 2)
                acao = yf.Ticker(ticker)
                preco_atual = round(acao.history(period='1d')['Close'][0], 5)
                valor_atual = round(preco_atual*quantidade, 2)
                lucro_prejuizo = round(valor_atual-valor_pago, 2)
                rentabilidade = round(lucro_prejuizo/valor_pago*100, 2)
                data_compra = datetime.strptime(data_compra_str, '%Y-%m-%d')
                if rentabilidade > 0:
                    status = "lucro"
                elif rentabilidade == 0:
                    status = "zero"
                else:
                    status = "prejuizo"
                hist = HistCripto(usuario_id=current_user.id, ticker = codigo, descricao=descricao, preco = preco_pago, quantidade=quantidade, valor=preco_pago*quantidade, tipo="compra", data=data_compra)
                nova_crypto = Crypto(ticker = codigo, preco_pago = preco_pago, quantidade = quantidade, valor_pago = valor_pago, preco_atual = preco_atual, valor_atual= valor_atual,rentabilidade= rentabilidade, lucro_prejuizo=lucro_prejuizo, data_compra = data_compra, status = status, usuario_id = current_user.id, link = link)
                db.session.add(hist)
                db.session.add(nova_crypto)
                db.session.commit()
                
                flash(f"{ticker} adicionada a carteira", category='success')
                return redirect(url_for('views.cryptos'))
            
    except:
        flash("Não foi possível!", category="error")
    return render_template("cripto/add_cripto.html", usuario = current_user)

#REMOVE CRIPTO
@views.route('/rm-cripto', methods= ['GET', 'POST'])
@login_required
def rm_cripto():
    try:
        if request.method == 'POST':
            ticker = request.form.get('ticker_venda')
            preco = float(request.form.get('preco_venda'))
            quantidade = int(request.form.get('quantidade_venda'))
            descricao = request.form.get('descricao_venda')
            data_str = request.form.get('dataVenda')    
            codigo = ticker.upper()
            data_venda = datetime.strptime(data_str, '%Y-%m-%d')
            qry = Crypto.query.filter_by(ticker=codigo).filter_by(usuario_id=current_user.id).first()
            if qry:
                qry.valor_pago = qry.valor_pago-(quantidade*qry.preco_pago)
                qry.quantidade = qry.quantidade-quantidade
                hist = HistCripto(usuario_id = current_user.id, ticker = codigo, descricao=descricao, preco= preco, quantidade=quantidade, valor = preco*quantidade, tipo="venda", data = data_venda)
                db.session.add(hist)
                db.session.commit()
                flash(f'{codigo} removida da carteira e adiconada ao histórico!', category="success")
            else: 
                flash("Cripto ou quantidade não foram encontradas", category='error')
        
    except:
        flash('Não foi possível!', category='error')
    return render_template('cripto/rm_cripto.html', usuario = current_user)

#TAREFA
@views.route('/tarefas', methods=["GET","POST"])
@login_required
def tarefas():
    return render_template("tarefa/tarefas.html", usuario = current_user)