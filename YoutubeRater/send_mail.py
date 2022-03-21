import smtplib
from email.message import EmailMessage

MAIL_USER, MAIL_PASS = "DoNotReplyRater", "AbcYOUTUBERATERprogram1!##"

def send_mail(subject, body, to, from_=None, host="smtp.gmail.com", port=587, addr=MAIL_USER, passw=MAIL_PASS):
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