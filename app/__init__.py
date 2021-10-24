from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# The API section is registered as a blueprint to make it portable as its own subsystem
from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')