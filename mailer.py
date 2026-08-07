import requests
import os
url = "https://api.brevo.com/v3/smtp/email"
apiKey=os.getenv("BR_API")

def send(typeOfMail, email, user, code=0):
     if typeOfMail=="regCode":
          sub="World of Industries Verification Code"
          with open("mailCode.html", 'r') as readBody:
                body=readBody.read()
          body=body.replace("verCode",str(code))
     elif typeOfMail=="regSuc":
          sub="Welcome onboard!"
          with open("mail.html", 'r') as readBody:
                body=readBody.read()

     payload = {
          "sender": {
               "name": "World of Industries Verification",
               "email": "verify@mail.woi.winnerworld.qzz.io"
      },
           "to": [
                {
                     "email": email,
                     "name": user
                }
            ],
            "params": {
               "avatarUrl": "https://aarushiswinner.qzz.io/woiLogo.png"
            },
            "replyTo": {
                 "email": "worldofindustriessup@gmail.com",
                 "name": "Support - World of Industries"
            },
            "htmlContent":body,
            "subject": sub
     }
     headers = {
          "accept": "application/json",
          "content-type": "application/json",
          "api-key": apiKey
     }

     response = requests.post(url, json=payload, headers=headers)

     print(eval(response.text))
     if "messageId" in eval(response.text).keys():
          return "Sent"
     else:
          return "Invalid"
