from flask_jwt_extended import create_access_token, get_jwt_identity
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from user.user_service import get_user_by_email, create_user, get_user_by_id
from utils.handler_errors import NotFoundException, BadRequestException
from utils.encrypt import verify_password
from datetime import timedelta
import os

days = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

def sign_in (body):
  try:
    user = get_user_by_email(body.email)
    if user is None:
      raise BadRequestException('email or password incorrect')

    id, _, user_email, password = user

    desencrypt = verify_password(body.password, password)

    if not desencrypt:
      raise BadRequestException('email or password incorrect')
    
    
    token = create_access_token(identity=user_email, fresh=True)
    refresh_token = create_access_token(identity=id, fresh=False, expires_delta=timedelta(days=days))

    response = jsonify({ 'refresh_token': refresh_token, 'token': token })
    response.set_cookie('access_token_cookie', refresh_token, httponly=True, secure=False)
    return response
  except SQLAlchemyError as e:
    raise e
  
def sign_up (body):
  try:
    user = get_user_by_email(body.email)
    if user:
      raise BadRequestException('this email already exists')
    return create_user(body)
  except NotFoundException as e:
    raise e
  
def refresh ():
  id = get_jwt_identity()
  user = get_user_by_id(id)
  token = create_access_token(identity=user[2], fresh=True)
  return jsonify({ 'refreshed_token': token })
  
def logout ():
  response = jsonify({ 'message': 'logout success' })
  response.set_cookie('access_token_cookie', '')
  return response