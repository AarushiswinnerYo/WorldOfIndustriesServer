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
import requests
import os
import mailer

cluster=os.getenv("MDB_CLUST")
client=MongoClient(cluster)
db=client.Users
names=db.mails
dbCount=client.WebView
counts=dbCount.Count
result=[]

app = Flask(__name__)
f=Fernet(os.getenv("FERNET_KEY").encode())
def refreshList():
    global result
    global correspondingEmails
    while True:
        l=[]
        r=[]
        for x in names.find():
            del x['_id']
            for e in x.keys():
                if e!="e":
                    l.append(f.decrypt(x[e].encode('utf-8')).decode())
                    r.append(f.decrypt(e.encode('utf-8')).decode())
                else:
                    pass
        result=r
        correspondingEmails=l
        time.sleep(1)

def main():
    global app

    @app.route('/')
    def home():
        t=request.args.get("t","")
        if t=="":
             return render_template('home.html')
        else:
             return render_template('home2.html')

    @app.route('/register')
    def my_form():
        return render_template('register.html')
    @app.route('/new')
    def count():
        red=request.args.get('red')
        t=request.args.get('t')
        r=counts.find_one({t:{"$exists":True}})
        d=counts.find_one({"count":{'$exists': True}})
        del d['_id']
        del r['_id']
        q=d['count']
        m=r[t]
        m+=1
        q+=1
        d['count']=q
        r[t]=m
        counts.delete_one({"count":{'$exists': True}})
        counts.insert_one(d)
        counts.delete_one({t:{'$exists': True}})
        counts.insert_one(r)
        return redirect(f"{red}?t={t}")
    @app.route('/ana')
    def showCount():
        d=counts.find_one({"count":{'$exists': True}})
        del d['_id']
        q=counts.find_one({"aarushiswinner":{'$exists': True}})
        del q['_id']
        d["aarushiswinner"]=q["aarushiswinner"]
        q=counts.find_one({"main":{'$exists': True}})
        del q['_id']
        d["main"]=q['main']
        q=counts.find_one({"winnerP":{'$exists': True}})
        d["winnerP"]=q['winnerP']
        return f"""<title>Analysis</title>{d}"""
    @app.route('/testing')
    def testingPage():
        return render_template("test.html")
    @app.route('/register', methods=['POST'])
    def my_form_post():
        mail = request.form['email']
        user=request.form['user']
        user=user.lower()
        mail = mail.lower()
        e=send(mail, user, "reg")
        if e=="Exist":
            return render_template("registerAgain.html", user=user)
        if e=="Email Exist":
            return render_template("registerAgainEmail.html", user=user)
        else:
            return redirect(url_for("veri", user=user))

    def send(senderAdd, username, typ):
        global usern
        def send_email(recipients, username, typ, code=0):
            if typ=="reg":
                mailer.send("regCode", recipients, username, code)
            else:
                mailer.send("regSuc", recipients, username)
            print("Message sent!")
        if typ=="reg":
            if username in result:
                return "Exist"
            elif senderAdd in correspondingEmails:
                return "Email Exist"
            else:
                code=random.randint(100000,999999)
                x=verCodes.verPend
                x[username.lower()]=code
                with open("verCodes.py", "w") as writeVer:
                        writeVer.write(f"verPend={x}")
                recipients = senderAdd
                result.append(username)
                usern = f.encrypt(username.encode('utf-8')).decode()
                senderAdd = f.encrypt(senderAdd.encode('utf-8')).decode()
                c={f"{usern}":f"{senderAdd}"}
                names.insert_one(c)
                send_email(recipients, username, "reg", code)
        elif typ=="codeVerd":
            recipients = senderAdd
            send_email(recipients, username, "codeVerd")

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
            d=names.find_one({f"{usern}": {'$exists': True}})
            mail=f.decrypt(d[usern]).decode('utf-8')
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
    t2=Thread(target=refreshList)
    t2.start()
    main()
        