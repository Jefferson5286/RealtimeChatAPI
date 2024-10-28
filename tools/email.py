from email.message import EmailMessage

from aiosmtplib import send
from decouple import config


async def send_confirm_code(email: str, code: str) -> None:
    #todo: implementar HTML personalizado para E-mails de confirmação.

    message = EmailMessage()

    message['From'] = 'no_repley@tredia.com'
    message['To'] = email
    message['Subject'] = 'Confirm Email'
    message.set_content(code)

    await send(
        message,
        hostname='smtp-relay.brevo.com',
        port=587,
        password=config('BREVO_PASSWORD'),
        start_tls=True,
        username=config('BREVO_LOGIN'),
    )
