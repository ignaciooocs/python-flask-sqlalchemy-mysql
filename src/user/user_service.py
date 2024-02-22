from database.db import connection
from flask import jsonify
from flask_jwt_extended import create_access_token
from entities.entities import users
from sqlalchemy.exc import SQLAlchemyError
from user.user_schema import CreateUser
from utils.encrypt import hash_password, verify_password
from utils.handler_errors import BadRequestException

def create_user(user: CreateUser):
  try:
    user.password = hash_password(user.password)

    result = connection.execute(users.insert().values({"name": user.name, "email": user.email, "password": user.password }))
    connection.commit()

    id, name, email, password = get_user_by_id(result.lastrowid)

    return { "id": id, "name": name, "email": email, "password": password }
  except Exception as e:
    raise e
  
def get_user_by_email (email):
  try:
    return connection.execute(users.select().where(users.c.email == email)).first()
  except SQLAlchemyError as e:
    raise e
  
def get_user_by_id (id):
  try:
    return connection.execute(users.select().where(users.c.id == id)).first()
  except SQLAlchemyError as e:
    raise e
  
def delete_user(email):
  try:
    connection.execute(users.delete().where(users.c.email == email))
    connection.commit()
    return '', 204
  except Exception as e: 
    raise e
  
def update_name(email, body):
  connection.execute(users.update().where(users.c.email == email).values({"name": body.name}))
  connection.commit()
  return jsonify({ 'message': 'user updated successfully' })

def update_email(email, body):
  user = get_user_by_email(body.email)
  if user:
    raise BadRequestException('this email already exists')
  
  connection.execute(users.update().where(users.c.email == email).values({"email": body.email }))
  connection.commit()
  token = create_access_token(identity=body.email)
  return jsonify({ 'token': token })

def update_password(email, body):
  if not verify_password(body.password, get_user_by_email(email)[3]):
    raise BadRequestException('password incorrect')
  
  hashed_password = hash_password(body.new_password)
  connection.execute(users.update().where(users.c.email == email).values({ "password": hashed_password }))
  connection.commit()
  return jsonify({ 'message': 'password updated successfully' })

