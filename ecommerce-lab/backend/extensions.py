from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_wtf import CSRFProtect
from flask_compress import Compress as FlaskCompress

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
admin = Admin(name='Celio Admin', template_mode='bootstrap4')
csrf = CSRFProtect()
compress = FlaskCompress()