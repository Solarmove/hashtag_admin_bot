import logging

from twilio.rest import Client

from configreader import config

client = Client(config.twilio_account_sid, config.twilio_auth_token)


async def send_sms(phone_number: str, message: str):
    message = client.messages.create(
        from_=config.twilio_phone_number,
        to=phone_number,
        body=message,
    )
    logging.info(f"SMS sent to {phone_number}")
    return message



