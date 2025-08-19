from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import verCodes
from cryptography.fernet import Fernet
import hashlib
from threading import Thread
from pymongo import MongoClient
import verEmails
import os

cluster=os.getenv("MDB_CLUST")
client=MongoClient(cluster)
db=client.Users
names=db.mails
result=[]
app = Flask(__name__)
f=Fernet(os.getenv("FERNET_KEY").encode())
for x in names.find():
    del x['_id']
    for e in x.keys():
        if e!="e":
            result.append(f.decrypt(e.encode('utf-8')).decode())
        else:
            pass

def main():
    global app

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/register')
    def my_form():
        return render_template('register.html')

    @app.route('/register', methods=['POST'])
    def my_form_post():
        mail = request.form['email']
        user=request.form['user']
        user=user.lower()
        mail = mail.lower()
        e=send(mail, user, "reg")
        if e=="Exist":
            return render_template("registerAgain.html", user=user)
        else:
            return redirect(url_for("veri", user=user))

    def send(senderAdd, username, typ):
        def send_email(subject, body, sender, recipients, password, typ):
            if typ=="reg":
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = ', '.join(recipients)
                msg.attach(MIMEText(body, "html"))
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(sender, password)
                    smtp_server.sendmail(sender, recipients, msg.as_string())
            else:
                msg = MIMEMultipart("alternative") 
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = ', '.join(recipients)
                msg.attach(MIMEText(body, "html"))
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                    smtp_server.login(sender, password)
                    smtp_server.sendmail(sender, recipients, msg.as_string())
            print("Message sent!")
        if typ=="reg":
            if username in result:
                return "Exist"
            else:
                code=random.randint(100000,999999)
                x=verCodes.verPend
                x[username]=code
                with open("verCodes.py", "w") as writeVer:
                        writeVer.write(f"verPend={x}")
                subject = "Email Verification"
                with open("mailCode.html","r") as readTemp:
                    body=readTemp.read()
                body = body.replace("verCode", str(code))
                sender = os.getenv("EMAIL")
                recipients = [senderAdd]
                password = os.getenv("EM_PASS")
                result.append(username)
                username = f.encrypt(username.encode('utf-8')).decode()
                senderAdd = f.encrypt(senderAdd.encode('utf-8')).decode()
                c={f"{username}":f"{senderAdd}"}
                names.insert_one(c)
                send_email(subject, body, sender, recipients, password, "reg")
        elif typ=="codeVerd":
            subject = "Email Verified"
            with open("mail.html","r") as readTemp:
                body=readTemp.read()
            sender = os.getenv("EMAIL")
            recipients = [senderAdd]
            password = os.getenv("EM_PASS")
            send_email(subject, body, sender, recipients, password, "codeVerd")

    @app.route('/veri')
    def veri():
        return render_template("veri.html", user=request.args.get('user'))
    
    @app.route('/veri', methods=['POST'])
    def veriPost():
        user=request.form['user']
        code=request.form["code"]
        user=user.lower()
        code=int(code)
        x=verCodes.verPend
        if x[user]==code:
            del x[user]
            with open("verCodes.py", "w") as writeVer:
                writeVer.write(f"verPend={x}")
            username=f.encrypt(user.encode('utf-8')).decode()
            d=names.find_one({f"{username}": {'$exists': True}})
            mail=f.decrypt(d[username]).decode('utf-8')
            send(mail, user, "codeVerd")
            user=user.title()
            return render_template("veried.html", user=user)
        else:
            return "Code was wrong"
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=10000)

def j():
    while True:
        t=names.find_one({"_id":"up"})
        print(t["e"])
        time.sleep(20)

if __name__ == "__main__":
    t1=Thread(target=j)
    t1.start()
    main()
        