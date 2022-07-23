import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
# from app.models import *

def send_email(to_address,subject,message):
    print("Trying to send a mail to:",to_address)
    # try:
    #     SMTP_SERVER_HOST='smtp.gmail.com'
    #     SMTP_SERVER_PORT=587
    #     SENDER_ADDRESS=os.getenv('email','something@gmail.com')
    #     SENDER_PASSWORD=os.getenv('password','<some-password>')
    #     msg=MIMEMultipart()
    #     msg['From']=SENDER_ADDRESS
    #     msg['To']=to_address
    #     msg['Subject']=subject
    #     msg.attach(MIMEText(message,'html'))
    #     s=smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
    #     s.starttls()
    #     s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    #     s.send_message(msg)
    #     s.quit()
    #     return True
    # except:
    SMTP_SERVER_HOST='0.0.0.0'
    SMTP_SERVER_PORT=1025
    SENDER_ADDRESS=os.getenv('email','viroop@chekuri.com')
    SENDER_PASSWORD=os.getenv('password')
    msg=MIMEMultipart()
    msg['From']=SENDER_ADDRESS
    msg['To']=to_address
    msg['Subject']=subject
    msg.attach(MIMEText(message,'html'))
    s=smtplib.SMTP(host=SMTP_SERVER_HOST,port=SMTP_SERVER_PORT)
    # s.starttls()
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg) #rom_addr, to_addrs, msg, mail_options=(), rcpt_options=()
    s.quit()
    return True

# def main():
#     new_users=[
#         {'name':'Viroo','email':'chekuriviroopaksh4950@gmail.com'}
#     ]
#     for user in new_users:
#         if send_email(user['email'],subject='Hello',message='Mailing you to remind that please revise your Decks'):
#             print("Mail sent!")

# if __name__ == '__main__':
#     main()