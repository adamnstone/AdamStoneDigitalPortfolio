import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail(username, password, text="Email Body", html=None, subject="Email Subject", from_email="from_email",
              to_emails=None, host="smtp.gmail.com", port=587):
    assert isinstance(to_emails, list)

    msg = MIMEMultipart("alternative")
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)
    msg["Subject"] = subject

    txt_part = MIMEText(text, "plain")
    msg.attach(txt_part)

    if html != None:
        html_part = MIMEText(html, "html")
        msg.attach(html_part)

    msg_str = msg.as_string()

    # log into smtp server
    with smtplib.SMTP(host=host, port=port) as server:
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_email, to_emails, msg_str)

