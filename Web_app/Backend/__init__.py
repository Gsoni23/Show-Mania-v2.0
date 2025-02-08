from flask import Flask
from flask_cors import CORS
from .database import db
from . import mail_flask
from flask_jwt_extended import JWTManager
from .api import api_bp
from werkzeug.security import generate_password_hash
from .cache import cache
DB_Name = "show-mania.sqlite"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'My_secret_key'
    app.config["JWT_SECRET_KEY"] = "super-secret"  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    db.init_app(app)
    CORS(app)
# ----------------- Cache Implementation-----------------
    cache.init_app(app)
    
#--------------- Configuring mail----------------- 
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'gsoni.2301@gmail.com' # Change it from your mail id
    app.config['MAIL_PASSWORD'] = 'drvrbgttdjghyalv' # Change the password accordingly.
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    mail_flask.mail.init_app(app)

    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(api_bp, url_prefix='/')



# ----------------- JWT Implementation-----------------
    from .models import User

    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def abc(user):
        return user

    @jwt.user_lookup_loader
    def abcd(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(user_id=identity).one_or_none()

# ----------------- Database Implementation-----------------
    with app.app_context():

        db.create_all()
        user = User.query.filter_by(email='govindsoni23engineer@gmail.com').first()
        if user:
            pass
        else:
            first_user = User(email = 'govindsoni23engineer@gmail.com', name = 'Govind Soni', password = generate_password_hash('admin1', method='scrypt'), isadmin = True)
            db.session.add(first_user)
            db.session.commit()

    app.app_context().push()


    return app