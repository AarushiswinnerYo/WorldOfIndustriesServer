import requests

url = "https://api.brevo.com/v3/smtp/email"
apiKey=os.environ.get("BR_API")

def send(code, typeOfMail, email, user):
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
               "email": "verify@worldofindustries.qzz.io"
      },
           "to": [
                {
                     "email": email,
                     "name": user
                }
            ],
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
     if "messageId" in eval(response).keys():
          return "Sent"
     else:
          return "Invalid Key"
