from flask_sqlalchemy import SQLAlchemy
from app import db
from model import users


class Members(db.Model):
    __tablename__ = 'members'

    id = db.Column('id', db.Integer, primary_key=True)
    channel_id = db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    is_admin = db.Column('is_admin', db.Boolean)

    def to_json(self):
        """Returns the instance of product as a JSON
        Returns:
            dict -- JSON representation of the product
        """
        return {
            'id': self.id,
            'channel_id': self.channel_id_id,
            'user_id': self.user_id,
            'is_admin': self.is_admin
        }