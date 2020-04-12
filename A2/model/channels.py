from flask_sqlalchemy import SQLAlchemy
from app import db
from model.members import Members
class Channels(db.Model):
    __tablename__ = 'channels'

    id= db.Column('id', db.Integer, primary_key=True)
    admin_id = db.Column('admin_id', db.Integer, db.ForeignKey('users.id'))
    name = db.Column('name', db.String(16))
    permalink = db.Column('permalink', db.String(16), unique=True)
    members = db.relationship('Members', backref='channel')

    def to_json(self):
        """Returns the instance of product as a JSON
        Returns:
            dict -- JSON representation of the product
        """
        return {
            'admin_id': self.admin_id,
            'name': self.name,
            'permalink': self.permalink,
        }