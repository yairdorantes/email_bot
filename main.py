import imaplib
import email
from email.header import decode_header
import time
import schedule
import requests

import os
from dotenv import load_dotenv

load_dotenv()

email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
webhook_url = os.getenv("WEBHOOK_URL")
imap_server = os.getenv("IMAP_SERVER")


print(
    "Initilizing values...",
    email_user,
    "|",
    email_pass,
    "|",
    webhook_url,
    " |",
    imap_server,
)


def check_unread_emails(username, password, imap_server=imap_server):
    try:
        # Conexión con el servidor IMAP en modo solo lectura
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)

        # Selecciona la bandeja de entrada (modo solo lectura)
        mail.select("inbox", readonly=True)

        # Busca correos no leídos
        status, messages = mail.search(None, "UNSEEN")
        if status != "OK":
            print("Error buscando correos no leídos.")
            return

        # Itera sobre los correos no leídos
        for num in messages[0].split():
            status, data = mail.fetch(num, "(BODY[HEADER.FIELDS (FROM SUBJECT DATE)])")
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    print(f"Nuevo correo de: {msg['From']}, Asunto: *{subject}*")
                    email_text = (
                        f"You got a new email from: {msg['From']}, Subject: *{subject}*"
                    )
                    send_whatsapp_message(email_text)

        mail.logout()

    except Exception as e:
        print(f"Error al revisar correos: {e}")


def check_emails():
    print("Checking for new emails...")
    check_unread_emails(email_user, email_pass)


def send_whatsapp_message(email_text: str):
    url = webhook_url
    data = {"new_email": email_text}
    response = requests.post(url, json=data)


schedule.every(1).hour.do(check_emails)

while True:
    schedule.run_pending()
    time.sleep(1)
