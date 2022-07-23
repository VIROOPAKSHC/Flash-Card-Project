from app.database import db
import datetime as dt
from flask_security import UserMixin,RoleMixin
from flask_security.utils import _security, get_hmac, _pwd_context

def verify_password(password, password_hash):
    """Returns ``True`` if the password matches the supplied hash.

    :param password: A plaintext password to verify
    :param password_hash: The expected hash value of the password (usually form your database)
    """
    if _security.password_hash != 'plaintext':
        password = get_hmac(password)

    return _pwd_context.verify(password, password_hash)


class Deck(db.Model):
  __tablename__='deck'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  name=db.Column(db.Integer,nullable=False)
  description=db.Column(db.String)


class Card(db.Model):
  __tablename__='card'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  front=db.Column(db.String,nullable=False)
  back=db.Column(db.String,nullable=False)
  DeckId=db.Column(db.Integer,db.ForeignKey('deck.id'),nullable=False)

roles_users=db.Table('roles_users',
db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
db.Column('role_id',db.Integer(),db.ForeignKey('role.id'))
)

class User(db.Model,UserMixin):
  __tablename__='user'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  email=db.Column(db.String,unique=True,nullable=False)
  # username=db.Column(db.String,unique=True)
  password=db.Column(db.String,nullable=False)
  last_reviewed=db.Column(db.String)
  active = db.Column(db.Boolean())
  fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
  roles=db.relationship('Role',secondary=roles_users,backref=db.backref('users',lazy='dynamic'))
  def check_password(self, password):
        return verify_password(password, self.password)

class Role(db.Model,RoleMixin):
  __tablename__='role'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  name=db.Column(db.String(80),unique=True)
  description=db.Column(db.String(255))


class UserCard(db.Model):
  __tablename__='usercard'
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,nullable=False)
  card_id=db.Column(db.Integer,db.ForeignKey('card.id'),primary_key=True,nullable=False)
  score=db.Column(db.Float,nullable=False)
  difficulty=db.Column(db.Integer)
  last_reviewed=db.Column(db.String)

class UserDeck(db.Model):
  __tablename__='userdeck'
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,nullable=False)
  deck_id=db.Column(db.Integer,db.ForeignKey('deck.id'),primary_key=True,nullable=False)
  score=db.Column(db.Float,nullable=False)
  last_reviewed=db.Column(db.String)
