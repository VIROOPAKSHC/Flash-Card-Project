from flask import Flask,render_template,request,redirect,make_response #Normal application making
from app.models import *
from app.database import *
from flask import session
from app import app
from flask_security.utils import login_user,logout_user
import flask
from flask_security import login_required
import uuid
import os
from flask import send_from_directory  
from flask_security import current_user
from app.tasks import *
# print("hi")   
# from flask.ext.bcrypt import Bcrypt

@app.route('/favicon.ico') 
def favicon(): 
  return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route("/registering")
def register():
  return render_template('register.html')
@app.route('/')
def login():
  return render_template('login.html')

@app.route('/dashboard',methods=['GET'])
def Dashboard():
  return render_template('Dashboard.html')
  


@app.route("/deck/<int:deckid>")
def ShowCards(deckid):
  return render_template("Cards.html")

@app.route('/addcard/<deckid>',methods=['GET','POST'])
 
def addcard(deckid):
  return render_template("AddCard.html")
@app.route('/editcard/<did>/<cid>',methods=['GET','POST'])
def editcard(did,cid):
  return render_template('EditCard.html')

@app.route('/AddDeck',methods=['GET','POST'])
def addDeck():
  return render_template('AddDeck.html')
@app.route('/editdeck/<did>',methods=['GET','POST'])
def editdeck(did):
  return render_template("EditDeck.html")
  

@app.route('/review')
@app.route('/Review')
def review():
  return render_template('Review.html')
  
@app.route('/review/<deckid>',methods=['GET','POST'])
def cardreview(deckid):
  return render_template('CardReview.html')

#START WORKERS USING:
# celery -A app.celery worker -l info
# celery -A main.celery beat --max-interval 1 -l info
# Switch on redis-server
# Switch on mail hog
# ~/go/bin/MailHog
# celery -A app.celery beat --max-interval 1 -l info
# 

@app.route('/export/deck/<id>',methods=['GET','POST'])
# Change where you used this route
def exporting(id):
  job=export.apply_async((id,current_user.id))
  result=job.wait()
  return redirect('/dashboard')

@app.route('/export',methods=['GET','POST'])
def exportDecks():
  job=export_decks.apply_async((current_user.id,))
  result=job.wait()
  # job.alert(result)
  return redirect('/dashboard')

@app.route('/export/cards/<deck_id>',methods=['GET','POST'])
def exportCards(deck_id):
  job=export_cards.apply_async((current_user.id,deck_id))
  result=job.wait()
  return redirect('/deck/'+str(deck_id))

@app.route('/import/<file_name>',methods=['GET','POST'])
def importing(file_name):
  data=open(file_name)
  form=json.load(data)
  print(form.keys())
  try:
    name=form['Name']
    description=form['Description']
    try:
      d=Deck.query.filter_by(name=name).one()
      return redirect('/AddDeck')
    except:
      pass
    deck=Deck(name=name,description=description)
    db.session.add(deck)
    c_id=0
    decks=Deck.query.filter_by(name=name).all()
    for deck in decks:
      try:
        udeck=UserDeck(user_id=current_user.id,deck_id=deck.id).one()
        continue
      except:
        c_id=deck.id
        break
    udeck=UserDeck(user_id=current_user.id,deck_id=c_id,score=0,last_reviewed=dt.datetime.now())
    db.session.add(udeck)
    if 'Cards' in form.keys():
      for card in form['Cards']:
        front=card['Front']
        back=card['Back']
        card=Card(front=front,back=back,DeckId=deck.id)
        db.session.add(card)
        card=Card.query.filter_by(front=front,back=back,DeckId=deck.id).one()
        ucard=UserCard(user_id=current_user.id,card_id=card.id,score=0,last_reviewed=dt.datetime.now())
        db.session.add(ucard)
    db.session.commit()
    return redirect("/dashboard")
  except Exception as e:
    print('Exception :',e)
    return redirect('/AddDeck')