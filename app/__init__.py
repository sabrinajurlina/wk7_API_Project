from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

#init plug-ins
login = LoginManager()
#init DB manager
db = SQLAlchemy()
migrate = Migrate()
moment = Moment()

def create_app(config_class=Config):
    #init the app
    app = Flask(__name__)
    #link in the Config
    app.config.from_object(config_class)

    #register plug-in
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    #configure some settings
    login.login_view = 'auth.login'
    login.login_message = 'Please log in'
    login.login_message_category='warning'

    from .blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app

