from app.workers import celery
import datetime as dt
from celery.schedules import crontab
from app.models import *
from flask import redirect
import json
from app.mail import *
@celery.on_after_finalize.connect
def reminder(sender,**kwargs):
    sender.add_periodic_task(crontab(minute=30,hour=17),remindertask.s(), name='Task to remind')
    # sender.add_periodic_task(crontab(),monthlyreport().s(), name='Task to remind')
    # sender.add_periodic_task(crontab(hour=22,minutes=52),remindertask.s(),name='Task to remind') #crontab(hour=20,minutes=54)
    pass


# can call these tasks using:
# celery -A app.celery call app.tasks.<task_name> --kwargs={'key':"value",}
# can link tasks using link=<function>.s()
# see celery chains for that

# gunicorn usage
# USAGE export ENV=stage
# gunicorn main:app --worker-class gevent --bind <host:port> --workers=<some integer>

@celery.task()
def remindertask():
    user=User.query.all()
    for u in user:
        if u.last_reviewed==None:
            send_email(u.email,'Reminder','Please revise your decks.\n You have not revised lately.')
        else:
            t1=dt.datetime.strptime(u.last_reviewed,"%Y-%m-%d %H:%M:%S.%f")
            t2=dt.datetime.now()
            diff=(t2-t1).total_seconds()
            diff=diff
            if diff>=1:
                send_email(u.email,'Reminder','Please revise your decks.\n You have not revised lately.')
            else:
                continue

@celery.task()
def monthlyreport():
    if dt.datetime.now().day!=1:
        return
    user=User.query.all()
    for u in user:
        send_email(u.email,'Progress','Your Monthly report')

@celery.task()
def print_current_time_job():
    print("START")
    now=dt.datetime.now()
    print("now =",now)
    dt_string=now.strftime("%d/%m/%Y %H:%M:%S")
    print("data and time =",dt_string)
    print('COMPLETE')
    return dt_string
    # Use this command in redis-cli
    # get celery-task-meta-<some-id>
    # get celery-task-meta-090743a2-c1ad-4f14-8013-31b486aedcea
@celery.task()
def export(id,user_id):
    user=User.query.filter_by(id=user_id).one()
    try:
        deck=Deck.query.filter_by(id=id).one()
        with open('Deck-'+str(deck.id)+'.csv','w') as f:
            f.write("Deck ID,Name,Description\n")
            f.write(str(deck.id)+","+deck.name+","+deck.description)
        return True
    except:
        try:
            card=Card.query.filter_by(id=id).one()
            with open('Card-'+str(card.id)+'.csv','w') as f:
                f.write('Card ID,Question,Answer\n')
                f.write(str(card.id)+','+card.front+","+card.back+'\n')
            return True
        except Exception as e:
            print('Exception :',e)
            return False

@celery.task()
def export_decks(user_id):
    user=User.query.filter_by(id=user_id).one()
    try:
        udeck=UserDeck.query.filter_by(user_id=user_id).all()
        with open('Decks-of-'+str(user_id)+".csv",'w') as f:
            f.write('Deck ID,Name,Description\n')

            for ud in udeck:
                deck=Deck.query.filter_by(id=ud.deck_id).one()
                f.write("{},{},{}\n".format(deck.id,deck.name,deck.description))
        return True
    except Exception as e:
        print('Exception :',e)
        return False

@celery.task()
def export_cards(user_id,deck_id):
    user=User.query.filter_by(id=user_id).one()
    try:
        # ucard=UserCard.query.filter_by(user_id=user_id).all()
        cards=Card.query.filter_by(DeckId=deck_id).all()
        with open('Cards-of-'+str(user_id)+'-'+str(deck_id)+'.csv','w') as f:
            f.write('Card ID,Question,Answer\n')
            for uc in cards:
                card=Card.query.filter_by(id=uc.id).one()
                f.write('{},{},{}\n'.format(card.id,card.front,card.back))
        return True
    except Exception as e:
        print('Exception :',e)
        return False
