from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from app import db
from model import users


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column('id', db.Integer, primary_key=True)
    channel_id = db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'))
    username = db.Column('username', db.String(32), db.ForeignKey('users.username'))
    content = db.Column('content', db.String(500))
    sent = db.Column('sent', db.DateTime, default=datetime.now)

    def to_json(self):
        """Returns the instance of product as a JSON
        Returns:
            dict -- JSON representation of the product
        """
        return {
            'channel_id': self.channel_id,
            'username': self.username,
            'content':self.content,
            'sent': self.sent
        }