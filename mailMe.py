from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import verCodes
import verEmails

app = Flask(__name__)

def main():
    global app
    @app.route('/')
    def my_form():
        return render_template('main.html')

    @app.route('/', methods=['POST'])
    def my_form_post():
        mail = request.form['email']
        user=request.form['user']
        user=user.lower()
        mail = mail.lower()
        send(mail, user, "reg")
        return redirect(url_for("veri", user=user))

    def send(senderAdd, username, typ):
        def send_email(subject, body, sender, recipients, password, typ):
            if typ=="reg":
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = sender
                msg['To'] = ', '.join(recipients)
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
            code=random.randint(100000,999999)
            x=verCodes.verPend
            x[username]=code
            with open("verCodes.py", "w") as writeVer:
                writeVer.write(f"verPend={x}")
            subject = "Email Verification"
            body = f"""Hello, {username.title()}!
This is your verification generated code: {code}"""
            sender = "worldofindustriessup@gmail.com"
            recipients = [senderAdd]
            password = "mddq wpsj eiyd olvs"
            e=verEmails.mailIDs
            e[username]=senderAdd
            with open("verEmails.py", "w") as writeVer:
                writeVer.write(f"mailIDs={e}")
            send_email(subject, body, sender, recipients, password, "reg")
        elif typ=="codeVerd":
            subject = "Email Verified"
            with open("mail.html","r") as readTemp:
                body=readTemp.read()
            sender = "worldofindustriessup@gmail.com"
            recipients = [senderAdd]
            password = "mddq wpsj eiyd olvs"
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
            f=verEmails.mailIDs
            mail=f[user]
            send(mail, user, "codeVerd")
            return render_template("veried.html", user=user)
        else:
            return "Code was wrong"
    app.run(host="0.0.0.0", debug=True, use_reloader=False, port=10000)

if __name__ == "__main__":
    main()
        