from flask_login import UserMixin
from .extensions import db, bcrypt

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class parking_spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pos_num = db.Column(db.Integer, nullable=False)

class Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, db.ForeignKey('parking_spot.pos_num'), nullable=False)
    pos = db.relationship('parking_spot', backref=db.backref('spot', uselist=False))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User', backref=db.backref('spot', uselist = False))
    avaliable = db.Column(db.Boolean, default=True)
    day = db.Column(db.String(20), nullable=False)