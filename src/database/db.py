from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URI'))

meta = MetaData()

def database_connection():
  try:
    connection = engine.connect()
    return connection
  except OperationalError as e:
    print(f"Error de conexión a la base de datos")
    raise e

# Establecer la conexión a la base de datos
connection = database_connection()