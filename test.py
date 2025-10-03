import requests

url = "https://api.brevo.com/v3/smtp/email"

payload = {
    "sender": {
        "name": "World of Industries Verification",
        "email": "verify@worldofindustries.qzz.io"
    },
    "replyTo": {
        "email": "worldofindustriessup@gmail.com",
        "name": "Support - World of Industries"
    },
    "to": [
        {
            "email": "aarushmusics@gmail.com",
            "name": "Aarushiswinner"
        }
    ],
    "htmlContent": "<h2 style=\"text-align: center;\"><span style=\"text-decoration: underline;\"><img src=\"https://aarushiswinner.qzz.io/woiLogo.png\" alt=\"\" width=\"250\" height=\"250\" /></span></h2> <h2 style=\"text-align: center;\"><span style=\"text-decoration: underline;\"><strong>Your E-Mail Verification code!</strong></span></h2> <p>Thank you for registering for our game!</p> <p>Here is your verification code: <strong>verCode</strong><br></p> <p>We hope you have a wonderful time!</p>",
    "subject": "Verification code"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "api-key": br-api
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)