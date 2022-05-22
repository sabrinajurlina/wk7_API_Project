from time import time
from app import db, login
from flask_login import UserMixin # IS ONLY FOR THE USER MODEL!!!!
from datetime import datetime as dt, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, index=True, unique=True)
    token_exp = db.Column(db.DateTime)

    ### ADD TOKEN METHODS HERE ###
    def get_token(self, exp=86400):
        current_time = dt.utcnow()
        if self.token and self.token_exp > current_time + timedelta(seconds=60):
            return self.token
        self.token = secrets.token_urlsafe(32)
        self.token_exp = current_time + timedelta(seconds=exp)
        self.save()
        return self.token

    def revoke_token(self):
        self.token_exp = dt.utcnow() - timedelta(seconds=61)

    @staticmethod
    def check_token(token):
        u = User.query.filter_by(token=token).first()
        if not u or u.token_exp < dt.utcnow():
            return None
        return u

    ### END TOKEN METHODS ###

    def __repr__(self):
        return f'<User: {self.email} | {self.id}>'
    
    def __str__(self):
        return f'<User: {self.email} | {self.first_name} {self.last_name}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_password_hash(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id':self.id,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'created_on':self.created_on,
            'is_admin':self.is_admin,
            'token':self.token,
            'token_exp':self.token_exp
        }

    def from_dict(self, data):
        for field in ['first_name','last_name','email','password', 'created_on', 'is_admin', 'token', 'token_exp']:
            if field == 'password':
                self.password = self.hash_password(data['password'])
            elif field in data:
                    #the object, the attribute, value
                setattr(self, field, data[field])

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

### END USER CLASS ###

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    author_first_name = db.Column(db.String)
    author_last_name = db.Column(db.String)
    pages = db.Column(db.Integer)
    summary = db.Column(db.String)
    image = db.Column(db.String)
    subject = db.Column(db.String)

    def __repr__(self):
        return f'<Book: {self.id} | {self.title}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author_first_name + ' ' + self.author_last_name,
            'pages': self.pages,
            'summary': self.summary,
            'image': self.image,
            'subject': self.subject
        }

    def from_dict(self, data):
        for field in ['title','author','pages','summary', 'image', 'subject']:
            if field in data:
                setattr(self, field, data[field])