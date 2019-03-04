import uuid

from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app import db


class Notebook(db.Model):
    __tablename__ = 'notebook'
    id = db.Column(UUID(), primary_key=True)
    name = db.Column(db.String(140), nullable=False)

    user_id = db.Column(UUID(), db.ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='notebooks', cascade='save-update, merge, delete')

    notes = relationship('Note', back_populates='notebook', cascade='save-update, merge, delete')

    creation_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='_user_notebook_uc'),
    )

    def __init__(self, name: str):
        self.id = uuid.uuid4().urn
        self.name = name

    def __repr__(self):
        return f'<Notebook {self.name}>'

    def __str__(self):
        return f'<Notebook {self.name}>'
