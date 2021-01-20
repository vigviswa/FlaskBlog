from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config
from flask_mail import Mail
import sshtunnel

app = Flask(__name__)
app.config.from_object(Config)

tunnel = sshtunnel.SSHTunnelForwarder(
    ("{IP Address of Tunnelling Instance}", 22),
    ssh_username="{Instance Username}",
    ssh_private_key="{PATH_TO_KEY_FILE}",
    remote_bind_address=("{Database Endpoint}", 3306),
)

tunnel.start()

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql://{username}:{password}@127.0.0.1:{}/flask".format(tunnel.local_bind_port)

db = SQLAlchemy(app)
brcypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "users.login_page"
login_manager.login_message_category = "info"

mail = Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)
