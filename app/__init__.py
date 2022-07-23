import json #Json (For APIs stuff)
import os #Managing modules directories etc
from flask import Flask
from flask_restful import Api
import logging
from flask_migrate import Migrate
from flask_login import LoginManager,login_required
from app.models import *  
from app.config import *
from app.database import db
from flask_sse import sse
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required
from flask import render_template
logging.basicConfig(filename='debug.log',level=logging.DEBUG,format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s')
celery=None
if os.getenv('ENV','development')=='production':
    raise Exception('Currently no production config is setup')
elif os.getenv('ENV','development')=='stage':
    app.logger.info('Starting Stage')
    print('Starting stage')
    app.config.from_object(StageConfig)
    print("Pushed config")

else:
    app=Flask(__name__)
    app.logger.info("Starting Local Development.")

    app.config.from_object(LocalDevelopmentConfig)
login_manager=LoginManager()
login_manager.init_app(app)

db.init_app(app)
app.app_context().push()
user_datastore=SQLAlchemyUserDatastore(db,User,Role)
security=Security(app, user_datastore)
migrate=Migrate(app,db)
api=Api(app)
app.app_context().push()

from app import workers
print("Workers setting up")
celery=workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
    timezone='Asia/Calcutta'
)
# celery.conf.enable_utc = False
celery.conf.timezone = "Asia/Calcutta"
celery.Task=workers.ContextTask
app.app_context().push()
app.register_blueprint(sse,url_prefix='/stream')
from app.controllers import *

from app.API import *  
#APIs
# api.add_resource(GetAPIList,'/api')
api.add_resource(UserAPI,'/getuserdetails') # GET method to obtain decks of a user.
api.add_resource(DeckAPI,'/user/<int:deck_id>','/user') # /user with POST , remaining with other
api.add_resource(DeckCardAPI,'/user/<int:deck_id>/<int:card_id>','/user/<int:deck_id>/cards')
api.add_resource(CardAPI,"/card/<int:deck_id>/<int:card_id>")
api.add_resource(AnswerAPI,"/answer/<int:deck_id>/<int:card_id>")
# run using this : flask run -h 0.0.0.0 -p 5000
