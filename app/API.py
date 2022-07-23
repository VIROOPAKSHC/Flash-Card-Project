from app.models import *
from app.database import db
from flask_restful import Resource,Api
from werkzeug.exceptions import HTTPException
from flask import request,make_response
import json
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required,current_user
session_logged_in=''
class NormalValidationError(HTTPException):
  def __init__(self,status_code,error_message,error_code):
    message={'error_code':error_code,'error_message':error_message}
    self.response=make_response( (message),status_code)

class ResourceCheck: 
  def deckcheck(deck_id):
    try:
      deck=Deck.query.filter_by(id=deck_id).one()
    except:
      raise NormalValidationError(404,'Deck does not exist','DECK001')
  def cardcheck(card_id):
    try:
      card=Card.query.filter_by(id=card_id).one()
    except:
      raise NormalValidationError(404,"Card does not exist",'CARD001')


class UserAPI(Resource):
  @auth_required("token")
  def get(self):
    try:
      userdecks=UserDeck.query.filter_by(user_id=current_user.id).all()
      deck_ids=[match.deck_id for match in userdecks]
      DeckList=[]
      for userdeck in userdecks:
        deck=Deck.query.filter_by(id=userdeck.deck_id).one()
        DeckList.append({"id":deck.id,"name":deck.name,"description":deck.description,"last_rev":str(userdeck.last_reviewed)[:19],"score":userdeck.score})
      return DeckList
    except:
      pass

class DeckAPI(Resource):
  @auth_required("token")
  def get(self,deck_id):
    try:
      ResourceCheck.deckcheck(deck_id=deck_id)
    except:
      raise NormalValidationError(404,"Deck does not exist","DECK001")
    try:
      deck=Deck.query.filter_by(id=deck_id).one()
      userdeck=UserDeck.query.filter_by(user_id=current_user.id,deck_id=deck_id).one()
      userdeck.last_reviewed=dt.datetime.now()
      return {"id":deck.id,"name":deck.name,"description":deck.description}
    except:
      raise NormalValidationError(404,'Deck does not belong to user','DECK002')
  @auth_required("token")
  def put(self,deck_id):
    try:
      ResourceCheck.deckcheck(deck_id=deck_id)
    except:
      raise NormalValidationError(404,"Deck does not exist","DECK001")
    try:  
      form=request.get_json()
      deck=Deck.query.filter_by(id=deck_id).one()
      deck.name=form['name']
      deck.description=form['description']
      userdeck=UserDeck.query.filter_by(user_id=current_user.id,deck_id=deck_id).one()
      userdeck.last_reviewed=dt.datetime.now()
      db.session.commit()
      return {"status":200}
    except:
      raise NormalValidationError(404,'Deck does not belong to user','DECK002')
  @auth_required("token")
  def delete(self,deck_id):
    try:
      ResourceCheck.deckcheck(deck_id=deck_id)
    except:
      raise NormalValidationError(404,"Deck does not exist","DECK001")
    try:
      userdeck=UserDeck.query.filter_by(user_id=current_user.id,deck_id=deck_id).one()
    except:
      raise NormalValidationError(404,'Deck does not belong to user','DECK002')
    
    for card in Card.query.filter_by(DeckId=deck_id):
      db.session.execute(f'delete from usercard where card_id={card.id};')
    db.session.execute(f'DELETE FROM card where DeckId={deck_id};')
    db.session.execute(f'DELETE FROM userdeck where user_id={current_user.id} and deck_id={deck_id};')
    db.session.execute(f'DELETE FROM deck where id={deck_id};')
    db.session.commit()
    return {"status_code":"Successfully deleted"}
  @auth_required("token")
  def post(self):
    
    form=request.get_json()
    if form==None:
      form=request.form
      print(form)
    try:
      name=form['name']
      description=form['description']
    except:
      raise NormalValidationError(404,'Wrong request body','REQUEST001')
    
    try:
      d=Deck.query.filter_by(name=name).one()
      return NormalValidationError(404,'Deck with given name already exists','DECK003')
    except:
      pass
    deck=Deck(name=name,description=description)
    db.session.add(deck)
    decks=Deck.query.filter_by(name=name).all()
    c_id=0
    for deck in decks:
      try:
        udeck=UserDeck(user_id=current_user.id,deck_id=deck.id).one()
        continue
      except:
        c_id=deck.id
        break
    udeck=UserDeck(user_id=current_user.id,deck_id=c_id,score=0,last_reviewed=dt.datetime.now())
    db.session.add(udeck)
    db.session.commit()
    deck=Deck.query.filter_by(name=name).one()
    return {"name":deck.name,"description":deck.description}

def calculateDeckScore(card_id,deck_id):
  userdeck=UserDeck.query.filter_by(deck_id=deck_id,user_id=current_user.id).one()
  total=0 
  d={1:0.4,2:0.7,3:1}
  sumtotal=0
  card_ids=[]
  for card in Card.query.filter_by(DeckId=deck_id).all():
    card_ids.append(card.id)
  for id in card_ids:
    usercard=UserCard.query.filter_by(user_id=current_user.id,card_id=id).one()
    sumtotal+=usercard.score*(d[usercard.difficulty])
    total+=1*(d[usercard.difficulty])
  userdeck.score=round((sumtotal/total)*100,3)
  userdeck.last_reviewed=dt.datetime.now()
  db.session.commit()
  return


class DeckCardAPI(Resource):
  @auth_required("token")
  def get(self,deck_id):
    ResourceCheck.deckcheck(deck_id=deck_id)
    try:
      usercards=UserCard.query.filter_by(user_id=current_user.id).all()
    except:
      raise NormalValidationError(404,'Card and Deck does not belong to user','CARD003')
    d=[]
    for usercard in usercards:
      card=Card.query.filter_by(id=usercard.card_id).one()
      if card.DeckId==deck_id:
        d.append({"id":card.id,"front":card.front,"back":card.back,"score":usercard.score,'last_reviewed':str(usercard.last_reviewed)[:19]})
    return d
   
  @auth_required("token")
  def put(self,deck_id,card_id):
    ResourceCheck.deckcheck(deck_id=deck_id)
    ResourceCheck.cardcheck(card_id=card_id)
    try:
      card=Card.query.filter_by(id=card_id).one()
      if card.DeckId!=deck_id:
        raise NormalValidationError(404,'Card does not belong to deck','CAD002')
    except:
        raise NormalValidationError(404,'Card does not exist','CARD001')
    
    try:
      usercard=UserCard.query.filter_by(card_id=card_id,user_id=current_user.id).one()
    except:
      raise NormalValidationError(404,'Card and Deck does not belong to user','CARD003')

    form=request.get_json()
    card.front=form['front']
    card.back=form['back']
    usercard=UserCard.query.filter_by(user_id=current_user.id,card_id=card_id).one()
    usercard.last_reviewed=dt.datetime.now()
    db.session.commit()
    card=Card.query.filter_by(id=card.id).one()
    return  ({"front":card.front,"back":card.back})
  
  @auth_required("token")
  def delete(self,deck_id,card_id):
    ResourceCheck.deckcheck(deck_id=deck_id)
    ResourceCheck.cardcheck(card_id=card_id)
    deck=Deck.query.filter_by(id=deck_id).one()
    try:
      card=Card.query.filter_by(id=card_id).one()
      if card.DeckId!=deck_id:
        raise NormalValidationError(404,'Card does not belong to deck','CARD002')
    except:
        raise NormalValidationError(404,'Card does not exist','CARD001')
    
    try:
      usercard=UserCard.query.filter_by(card_id=card_id,user_id=current_user.id).one()
    except:
      raise NormalValidationError(404,'Card and Deck does not belong to user','CARD003')

    db.session.execute(f'delete from usercard where user_id={current_user.id} and card_id={card_id};')
    db.session.execute(f'delete from card where id={card_id};')
    db.session.commit()
    return {"status_code":"successfully deleted"}

  @auth_required("token")
  def post(self,deck_id):
    ResourceCheck.deckcheck(deck_id=deck_id)
    form=request.get_json()
    
    try:
      userdeck=UserDeck.query.filter_by(user_id=current_user.id,deck_id=deck_id).one()
    except:
      raise NormalValidationError(404,'Deck does not belong to user','DECK002')
    front=form['front']
    back=form['back']
    card=Card(front=front,back=back,DeckId=deck_id)
    db.session.add(card)
    card=Card.query.filter_by(front=front,back=back,DeckId=deck_id).one()
    ucard=UserCard(user_id=current_user.id,card_id=card.id,score=0,last_reviewed=dt.datetime.now())
    db.session.add(ucard)
    db.session.commit()
    return {"front":card.front,"back":card.back}

class CardAPI(Resource):
  @auth_required("token")
  def get(self,deck_id,card_id):
    # userdeck=UserDeck.query.filter_by(user_id=current_user.id,deck_id=deck_id).one()
    ResourceCheck.deckcheck(deck_id)
    ResourceCheck.cardcheck(card_id)
    try:
      usercard=UserCard.query.filter_by(user_id=current_user.id,card_id=card_id).one()
      card=Card.query.filter_by(DeckId=deck_id,id=card_id).one()
      return {"front":card.front,"back":card.back,"score":usercard.score,"last_reviewed":str(usercard.last_reviewed)[:19]}
    except:
      raise NormalValidationError(404,"Card does not belong to the user",'CARD002')
class AnswerAPI(Resource):
  @auth_required("token")
  def post(self,deck_id,card_id):
    ResourceCheck.deckcheck(deck_id)
    ResourceCheck.cardcheck(card_id)
    
    try:
      form=request.get_json()
      # print(form)
      if 'front' in form.keys():
        question=form['front']
        c=Card.query.filter_by(id=card_id).one()
        user=User.query.filter_by(id=current_user.id).one()
        answer=form['answer']
        difficulty= form.get('Difficulty')
        usercard=UserCard.query.filter_by(user_id=current_user.id,card_id=c.id).one()
        if difficulty:
          if difficulty[0]=='Hard':
            difficulty=3
          elif difficulty[0]=='Medium':
            difficulty=2
          else:
            difficulty=1
       
          if "".join(answer.lower().split())=="".join(c.back.lower().split()):
            usercard.score=1
            usercard.difficulty=difficulty
          else:
            usercard.difficulty=difficulty
            usercard.score=0
        else:
          if "".join(answer.lower().split())=="".join(c.back.lower().split()):
            usercard.score=1
          else:
            usercard.score=0
      
        user.last_reviewed=dt.datetime.now()
        usercard.last_reviewed=dt.datetime.now()
        calculateDeckScore(card_id=c.id,deck_id=deck_id)
        db.session.commit()
        result=Card.query.filter_by(DeckId=deck_id).all()
       
        return {'status_code':200}
      else:
        c=Card.query.filter_by(id=card_id).one()
        difficulty= form['Difficulty']
        print(form,difficulty)
        if difficulty[0]=='Hard':
          difficulty=3
        elif difficulty[0]=='Medium':
          difficulty=2
        else:
          difficulty=1
        
        usercard=UserCard.query.filter_by(user_id=current_user.id,card_id=c.id).one()
        usercard.difficulty=difficulty
        user=User.query.filter_by(id=current_user.id).one()
        user.last_reviewed=dt.datetime.now()
        
        usercard.last_reviewed=dt.datetime.now()
        calculateDeckScore(card_id=c.id,deck_id=deck_id)
        db.session.commit()
        return {'status_code':200}
    except Exception as e:
      print(e)
      raise NormalValidationError(400,"Bad Request","REQUEST001")
