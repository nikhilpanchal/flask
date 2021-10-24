from flask.json import jsonify
from app.api import bp
from app.models import User

"""
Since the api section is defined as a blueprint we will use @bp.route as the decorator to register these
api *handler* functions. 

Additionally, if you look in the app.__init__.py file, you'll see the api blueprint is registered at the 
url_prefix of '/api' which will get pre-pended to each of the routes defined in this file #prettyneat
"""

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
def users():
    pass

@bp.route('/users/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass

@bp.route('/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass

@bp.route('/users', methods=['GET'])
def create_user():
    pass

@bp.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    pass