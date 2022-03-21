import smtplib
from email.message import EmailMessage

def send_mail(addr, passw, subject, body, to, from_=None, host="smtp.gmail.com", port=587):
    msg = EmailMessage()
    msg.set_content(body)

    msg['Subject'] = subject
    msg['From'] = addr if from_ is None else from_
    msg['To'] = to

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(addr, passw)
    server.send_message(msg)
    server.quit()