from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from datetime import datetime
from website import db
from .models import Usuario, CarteiraCripto, CarteiraAcoes, Conta
auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario:
            if usuario.senha == senha:
                flash("Login efetuado!", category='success')
                login_user(usuario, remember=True)
                return redirect(url_for('views.home'))

            else:
                flash("Senha incorreta. Tente novamente.", category='error')
        else:
            flash('Email não existe!', category='error')
    
    return render_template("auth/login.html")

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        nome = request.form.get('nome')
        senha = request.form.get('senha')
        senha2 = request.form.get('senha2')

        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            flash('Email já cadastrado!', category='error')
        elif len(email) < 4:
            flash('Email deve ter pelo menos 4 caracteres', category='error')
        elif len(nome) < 2:
            flash('Nome deve ter pelo menos 2 caracteres', category='error')
        elif senha != senha2:
            flash('Senhas não conferem', category='error')
        elif len(senha) < 7:
            flash('Senha deve ter pelo menos 7 caracteres', category='error')
        else:
            current_time = datetime.now()
            usuario = Usuario(email=email, nome = nome, senha = senha)
            db.session.add(usuario)
            db.session.commit()
            carteira_acoes = CarteiraAcoes(usuario_id = usuario.id, valor_pago_total = 0, valor_atual_total = 0, lucro_prejuizo = 0, rentabilidade_total = 0, status = "zero", total_dividendos = 0)
            carteira_cripto = CarteiraCripto(usuario_id = usuario.id, valor_pago_total = 0, valor_atual_total = 0, lucro_prejuizo = 0, rentabilidade_total = 0, status = "zero")
            conta = Conta(usuario_id = usuario.id, saldo = 0, criacao = current_time)
            db.session.add(carteira_acoes)
            db.session.add(carteira_cripto)
            db.session.add(conta)
            db.session.commit()
            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))

    return render_template("auth/sign_up.html")