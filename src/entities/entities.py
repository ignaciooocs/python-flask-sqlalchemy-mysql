from sqlalchemy import Table, Column, Integer, String, Boolean, ForeignKey
from database.db import engine, meta

users = Table(
  'users',
  meta,
  Column('id', Integer, primary_key=True),
  Column('name', String(255)),
  Column('email', String(255), unique=True),
  Column('password', String(255))
)

notes = Table(
  'notes',
  meta,
  Column('id', Integer, primary_key=True),
  Column('title', String(255), nullable=False),
  Column('content', String(255), nullable=False),
  Column('priority', Boolean, default=False),
  Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
)

meta.create_all(engine)