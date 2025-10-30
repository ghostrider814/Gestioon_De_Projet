from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_wtf import CSRFProtect
from flask_compress import Compress as FlaskCompress
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
admin = Admin(name='Celio Admin')  # Supprimé template_mode
csrf = CSRFProtect()
compress = FlaskCompress()
mail = Mail()
