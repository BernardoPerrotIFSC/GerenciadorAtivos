from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from . import admin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique= True)
    senha = db.Column(db.String(100))
    nome = db.Column(db.String(150))
    total = db.Column(db.Float)
    total_acoes = db.Column(db.Float)
    total_criptos = db.Column(db.Float)
    total_criptosR = db.Column(db.Float)
    acoes = db.relationship('Acao')
    cryptos = db.relationship('Crypto')
    carteira_acoes = db.relationship('CarteiraAcoes')
    carteira_cripto = db.relationship('CarteiraCripto')
    conta = db.relationship('Conta')
    hist = db.relationship('HistTransacoes')
    hist_acao = db.relationship('HistAcao')
    hist_cripto = db.relationship('HistCripto')

class Acao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    preco_pago = db.Column(db.Float)
    valor_pago = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    data_compra = db.Column(db.Date)
    preco_atual = db.Column(db.Float)
    valor_atual = db.Column(db.Float)
    lucro_prejuizo = db.Column(db.Float)
    rentabilidade = db.Column(db.Float)
    status = db.Column(db.String)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    link = db.Column(db.String)
    last_yield = db.Column(db.Float)
    total_dividends = db.Column(db.Float)
    yield_total = db.Column(db.Float)

class Dividendos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    data_compra = db.Column(db.Date)
    last_dividend = db.Column(db.Float)
    total = db.Column(db.Float)

class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10))
    preco_pago = db.Column(db.Float)
    valor_pago = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    data_compra = db.Column(db.Date)
    preco_atual = db.Column(db.Float)
    valor_atual = db.Column(db.Float)
    lucro_prejuizo = db.Column(db.Float)
    rentabilidade = db.Column(db.Float)
    status = db.Column(db.String)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    link = db.Column(db.String)

class CarteiraCripto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    valor_pago_total = db.Column(db.Float)
    valor_atual_total = db.Column(db.Float)
    lucro_prejuizo = db.Column(db.Float)
    rentabilidade_total = db.Column(db.Float)
    status = db.Column(db.String)
    last_update = db.Column(db.Date, nullable=True)

class CarteiraAcoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    valor_pago_total = db.Column(db.Float)
    valor_atual_total = db.Column(db.Float)
    lucro_prejuizo = db.Column(db.Float)
    rentabilidade_total = db.Column(db.Float)
    status = db.Column(db.String)
    total_dividendos = db.Column(db.Float, nullable=True)
    last_update = db.Column(db.Date, nullable=True)

class Conta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    saldo = db.Column(db.String)
    criacao = db.Column(db.Date)

class HistTransacoes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    descricao = db.Column(db.String)
    valor = db.Column(db.Float)
    tipo = db.Column(db.String)
    data = db.Column(db.Date)

class HistCripto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ticker = db.Column(db.String)
    descricao = db.Column(db.String)
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Float)
    valor = db.Column(db.Float)
    tipo = db.Column(db.String)
    data = db.Column(db.Date)

class HistAcao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    ticker = db.Column(db.String)
    descricao = db.Column(db.String)
    preco = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.Float)
    tipo = db.Column(db.String)
    data = db.Column(db.Date)

admin.add_view(ModelView(Usuario, db.session))
admin.add_view(ModelView(Acao, db.session))
admin.add_view(ModelView(Crypto, db.session))
admin.add_view(ModelView(CarteiraCripto, db.session))
admin.add_view(ModelView(CarteiraAcoes, db.session))
admin.add_view(ModelView(Conta, db.session))
admin.add_view(ModelView(HistAcao, db.session))
admin.add_view(ModelView(HistCripto, db.session))
admin.add_view(ModelView(HistTransacoes, db.session))
