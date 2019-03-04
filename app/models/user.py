import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(UUID(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    name_lower = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    notebooks = relationship('Notebook', back_populates='user', cascade='save-update, merge, delete')
    notes = relationship('Note', back_populates='user', cascade='save-update, merge, delete')

    def __init__(self, name: str, email: str):
        self.id = uuid.uuid4().urn
        self.name = name
        self.name_lower = name.lower()
        self.email = email.lower()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.name}>'

    def __str__(self):
        return f'<User {self.name}>'
