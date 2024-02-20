from os import path
from flask import Flask, session
# from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from google_login.config import Config, DB_NAME
from .models import User, db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    from google_login.views import views

    app.register_blueprint(views, url_prefix='/')
    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app


def create_database(app):
    if not path.exists('google_login/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


app = create_app()


if __name__ == "__main__":
    context = (app.config['SSL_CERTIFICATE'], app.config['SSL_KEY'])
    app.run(debug=True, ssl_context=context)
