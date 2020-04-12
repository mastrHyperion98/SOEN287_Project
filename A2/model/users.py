from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db
from model import channels
class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.UniqueConstraint('id', 'email', 'username', 'permalink', name='user_uc'),
    )
    id=db.Column('id', db.Integer, primary_key=True)
    email=db.Column('email', db.String(50))
    password=db.Column('password', db.String(32))
    username=db.Column('username', db.String(32))
    permalink=db.Column('permalink', db.String(16))
    login=db.Column('login', db.DateTime, default=datetime.now)
    channels = db.relationship('channels', backref='admin')

    def to_json(self):
            """Returns the instance of product as a JSON
            Returns:
                dict -- JSON representation of the product
            """
            return {
                'id': self.id,
                'email': self.email,
                'username': self.username,
                'permalink': self.permalink,
                'login': str(self.login)
            }