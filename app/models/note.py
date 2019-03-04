import uuid

from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app import db


class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(UUID(), primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.String(2048), nullable=False)

    notebook_id = db.Column(UUID(), db.ForeignKey('notebook.id'))
    notebook = relationship('Notebook', back_populates='notes', cascade='save-update, merge, delete')

    user_id = db.Column(UUID(), db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='notes')

    creation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, name: str, description: str):
        self.id = uuid.uuid4().urn
        self.name = name
        self.description = description

    def __repr__(self):
        return f'<Note {self.name}>'

    def __str__(self):
        return f'<Note {self.name}>'
