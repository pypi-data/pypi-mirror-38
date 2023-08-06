import smtplib

class TextMessageSession:
    def __init__(self, smtpAddress, email, password):
        self.server = smtplib.SMTP(smtpAddress, 587)
        self.server.starttls()
        self.server.login(email, password)
        self.email = email

    def sendText(carrierAddress, phoneNumber, message):
        self.server.sendmail(email, phoneNumber + carrierAddress, message)

