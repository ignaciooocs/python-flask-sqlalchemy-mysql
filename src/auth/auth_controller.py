from flask import Blueprint, jsonify
from flask_pydantic import validate
from sqlalchemy.exc import SQLAlchemyError
from user.user_schema import CreateUser
from auth.auth_schemas.sign_in_schema import SignIn
from auth.auth_service import sign_in, sign_up, logout, refresh
from flask_jwt_extended import jwt_required

auth = Blueprint('auth', __name__)

@auth.route('/sign-in', methods=['POST'])
@validate(body=SignIn)
def signin(body: SignIn):
  try:
    return sign_in(body)
  except SQLAlchemyError as e:
      return jsonify(error=str(e)), 500
    
@auth.route('/sign-up', methods=['POST'])
@validate(body=CreateUser)
def signup(body: CreateUser):
  return sign_up(body)

@auth.route('/refresh')
@jwt_required(locations='cookies')
def refresh_controller():
  return refresh()

@auth.route('/logout')
def logout_controller():
  return logout()

