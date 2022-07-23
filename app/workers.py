from celery import Celery
from app import app
celery=Celery('Application Jobs')

class ContextTask(celery.Task):
    def __cal__(self,*args,**kwargs):
        with app.app_context():
            return self.run(*args,**kwargs)