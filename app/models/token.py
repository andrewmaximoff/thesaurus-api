import uuid

from sqlalchemy.dialects.postgresql import UUID

from app import db


class TokenBlacklist(db.Model):
    # TODO: Token has life time, better keep it in Redis
    __tablename__ = 'token_blacklist'

    id = db.Column(UUID(), primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        super(TokenBlacklist, self).__init__(*args, **kwargs)
        self.id = uuid.uuid4().urn

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }
