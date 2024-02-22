from flask.blueprints import Blueprint
from flask_pydantic import validate
from flask_jwt_extended import jwt_required, get_jwt
from notes.note_service import create_note, get_all_by_user_id, delete_note, update_title, update_content, update_priority
from notes.note_schema import CreateNote, UpdateTitle, UpdateContent, UpdatePriority

note = Blueprint('note', __name__)

@note.route('/')
@jwt_required(locations='headers')
def get_all_by_user_id_controller():
  return get_all_by_user_id()

@note.route('/', methods=['POST'])
@jwt_required(locations='headers')
@validate(body=CreateNote)
def create_note_controller(body: CreateNote):
  print(get_jwt())
  return create_note(body)

@note.route('/<int:id>', methods=['DELETE'])
@jwt_required(locations='headers')
def delete_note_controller(id):
  return delete_note(id)

@note.route('/title/<int:id>', methods=['PUT'])
@jwt_required(locations='headers')
@validate(body=UpdateTitle)
def update_note_title_controller(body: UpdateTitle, id: int):
  print(body)
  return update_title(id, body.title)


@note.route('/content/<int:id>', methods=['PUT'])
@jwt_required(locations='headers')
@validate(body=UpdateContent)
def update_note_content_controller(body: UpdateContent, id: int):
  return update_content(id, body.content)

@note.route('/priority/<int:id>', methods=['PUT'])
@jwt_required(locations='headers')
@validate(body=UpdatePriority)
def update_note_priority_controller(body: UpdatePriority, id: int):
  return update_priority(id, body.priority) 