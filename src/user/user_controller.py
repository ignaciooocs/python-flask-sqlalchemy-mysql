from flask.blueprints import Blueprint
from user.user_service import update_name, update_email, update_password, delete_user
from user.user_schema import UpdateName, UpdateEmail, UpdatePassword
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt_identity

user = Blueprint('user', __name__)

@user.route('/', methods=['DELETE'])
@jwt_required(locations='headers')
def delete_user_controller():
  email = get_jwt_identity()
  return delete_user(email)

@user.route('/name', methods=['PUT'])
@jwt_required(locations='headers')
@validate(body=UpdateName)
def update_name_controller (body: UpdateName):
  email = get_jwt_identity()
  return update_name(email, body)

@user.route('/email', methods=['PUT'])
@jwt_required(locations='headers')
@validate(body=UpdateEmail)
def update_email_controller (body: UpdateEmail):
  email = get_jwt_identity()
  return update_email(email, body)

@user.route('/password', methods=['PUT'])
@jwt_required(locations='headers')
@validate(body=UpdatePassword)
def update_password_controller (body: UpdatePassword):
  email = get_jwt_identity()
  return update_password(email, body)

