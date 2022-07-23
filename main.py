try:
  from app import app
except Exception as e:
  print("THIS IS AN ERROR",e)
if __name__=="__main__":
  app.run()