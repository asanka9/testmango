# doing necessary imports

from flask import Flask, render_template, request,jsonify,flash,redirect,url_for
# from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo
import time
import smtplib
from email.message import EmailMessage
import datetime


app = Flask(__name__)  # initialising the flask app with the name 'app'
adminrun = False

@app.route('/admin') # route with allowed methods as POST and GET
def admin():
    client = pymongo.MongoClient("mongodb+srv://asanka:asanka96@scrapper.pelc0.mongodb.net/test")
    myDB = client['userDB']
    collection = myDB.tablenamecollection
    while(True):
        searchScrap(collection)
        time.sleep(1)

def searchScrap(collection):
    for record in collection.find({}):
        uClient = uReq(record['url'])
        page = uClient.read()
        uClient.close()
        flipkart_html = bs(page, "html.parser")
        i = 0
        for tag in record['tags']:
            try:
                bigboxes = flipkart_html.findAll(record['elements'][i], {"class": tag})
                print('******************************')
                print(record['url'])
                print(record['email'])
                print(tag)
                print(len(bigboxes))
                print('******************************')
                if(len(bigboxes)==0):
                    message = ''
                    send_email('wassoftasanka@gmail.com', 'subjects', 'message')
            except:
                continue
        return 'admin '



def send_email(receiver, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Make sure to give app access in your Google account
    server.login('sendasanka96@gmail.com', 'asanka@96')
    email = EmailMessage()
    email['From'] = 'Sender_Email'
    email['To'] = receiver
    email['Subject'] = subject
    email.set_content(message)
    server.send_message(email)



@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():

    if request.method == 'POST':
        email = request.form['email'].replace(" ","")
        url = request.form['url'].replace(" ","")
        elements = request.form['elements'].replace(" ","")
        tags = request.form['tags'].replace(" ","")
        try:
            dbConn = pymongo.MongoClient("mongodb+srv://asanka:asanka96@scrapper.pelc0.mongodb.net/test")  # opening a connection to Mongo
            db = dbConn['userDB'] # connecting to the database called crawlerDB
            collection = db.tablenamecollection
            record = {
                'email': email,
                'url': url,
                'elements':elements.split(','),
                'tags':tags.split(',')
            }
            collection.insert_one(record)
            flash('this is  checked', 'info')

            return redirect(url_for('index'))

        except:
            return 'something is wrong'
            #return render_template('results.html')
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True) # running the app on the local machine on port 8000

