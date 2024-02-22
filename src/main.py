from flask import Flask, json, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager
from auth.auth_controller import auth
from user.user_controller import user
from notes.note_controller import note
from utils.handler_errors import NotFoundException, BadRequestException, UnauthorizedException
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app, resources={r"/*": { "origins": [os.getenv('ORIGINS1'), os.getenv('ORIGINS2')] }}, supports_credentials=True)
load_dotenv()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

app.config['JWT_TOKEN_LOCATION'] = ['cookies', 'headers']
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
# app.config['JWT_COOKIE_SECURE'] = False  # En producción, deberías configurarlo en True
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # En producción, deberías configurarlo en True

JWT = JWTManager(app)

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

@app.errorhandler(NotFoundException)
def handle_not_found_error(e):
    return jsonify({"description": str(e), "status": 404, "name": "Not found"}), 404

@app.errorhandler(BadRequestException)
def handle_bad_request_error(e):
    return jsonify({"description": str(e), "status": 400, "name": "Bad request"}), 400

@app.errorhandler(UnauthorizedException)
def handle_unauthorized_error(e):
    return jsonify({"description": str(e), "status": 401, "name": "Unauthorized"}), 401

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(note, url_prefix='/notes')

if __name__ == '__main__':
  app.run(debug=True)