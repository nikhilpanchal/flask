from flask import Blueprint

# __name__ here is 'app.api'
bp = Blueprint('api', __name__)

from app.api import users, errors, tokens
