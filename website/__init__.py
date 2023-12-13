from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

db = SQLAlchemy()
DB_NAME = "database.db"
admin = Admin()

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'você não vai advinhar'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    admin.init_app(app)
    migrate = Migrate(app, db)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Usuario, Acao

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message= 'Faça o login para acessar esta página.'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))

    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Banco de dados criado.')