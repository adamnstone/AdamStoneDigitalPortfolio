import imaplib, email, os, strip_rtf

ATTACHMENTS_DIR = "attachments/"

def get_inbox(username, password, host="imap.gmail.com", amount_of_emails_func = lambda x: x):
    mail = imaplib.IMAP4_SSL(host)
    mail.login(username, password)
    mail.select("inbox")

    attachment_string_to_return = None

    _, search_data = mail.search(None, "ALL")
    my_messages = []
    for num in amount_of_emails_func(search_data[0].split()):
        email_data = {}
        _, data = mail.fetch(num, "(RFC822)")
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ["subject", "to", "from", "date"]:
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data["body"] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data["html_body"] = html_body.decode()
            if not part.get_content_maintype() == "multipart":
                if not part.get("Content-Disposition") is None:
                    file_name = part.get_filename()
                    if file_name[-len(".rtf"):] == ".rtf":
                        print(file_name)
                        if bool(file_name):
                            if not os.path.exists(ATTACHMENTS_DIR):
                                os.makedirs(ATTACHMENTS_DIR)
                            rtf = part.get_payload(decode=True)
                            attachment_string_to_return = strip_rtf.striprtf(rtf)
                    elif file_name[-len(".txt"):] == ".txt":
                        attachment_string_to_return = part.get_payload(decode=True).decode()
                    elif file_name[-len(".html"):] == ".html":
                        attachment_string_to_return = part.get_payload(decode=True).decode()
        my_messages.append(email_data)

    return my_messages, attachment_string_to_return
