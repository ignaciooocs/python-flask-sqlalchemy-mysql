from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from database.db import connection
from entities.entities import notes
from user.user_service import get_user_by_email
from utils.handler_errors import NotFoundException
  
def create_note(note):
  try:
    email = get_jwt_identity()
    user = get_user_by_email(email)

    if not user:
      raise NotFoundException('user not found')

    result = connection.execute(notes.insert().values({"title": note.title, "content": note.content, "priority": note.priority, "user_id": user[0] }))
    connection.commit()
    return get_one(result.lastrowid)
  except Exception as e:
    raise e
  
def get_one(id):
  try:
    note_found = connection.execute(notes.select().where(notes.c.id == id)).first()
    
    if not note_found:
      raise NotFoundException('note not found')
    note = dict({ "id": note_found[0], "title": note_found[1], "content": note_found[2], "priority": note_found[3], "user_id": note_found[4] })
    return note
  except Exception as e:
    raise e
  
def get_all_by_user_id ():
  try:
    all_notes = []

    email = get_jwt_identity()
    user = get_user_by_email(email)

    notes_founded = connection.execute(notes.select().where(notes.c.user_id == user[0])).fetchall()

    for n in notes_founded:
      all_notes.append({ "id": n[0], "title": n[1], "content": n[2], "priority": n[3], "user_id": n[4] })

    return jsonify(all_notes)
  except Exception as e:
    raise e

def delete_note(id):
  try:
    email = get_jwt_identity()
    user = get_user_by_email(email)

    connection.execute(notes.delete().where(notes.c.id == id and notes.c.user_id == user[0]))
    connection.commit()
    return '', 204
  except Exception as e: 
    raise e
  
def update_title(id, title):
  try:
    email = get_jwt_identity()
    user = get_user_by_email(email)

    connection.execute(notes.update().where(notes.c.id == id and notes.c.user_id == user[0]).values({"title": title}))
    connection.commit()
    return get_one(id)
  except Exception as e:
    raise e
  
def update_content(id, content):
  try:
    email = get_jwt_identity()
    user = get_user_by_email(email)

    connection.execute(notes.update().where(notes.c.id == id and notes.c.user_id == user[0]).values({"content": content}))
    connection.commit()
    return get_one(id)
  except Exception as e:
    raise e

def update_priority (id, priority):
  try:
    email = get_jwt_identity()
    user = get_user_by_email(email)

    connection.execute(notes.update().where(notes.c.id == id and notes.c.user_id == user[0])).values({ "priority": priority })
    connection.commit()
    return get_one(id) 
  except Exception as e:
    raise e