import logging

from twilio.rest import Client

from configreader import config

client = Client(config.twilio_account_sid, config.twilio_auth_token)


async def send_sms(phone_number: str, message: str):
    message = client.messages.create(
        messaging_service_sid="MG3fb0b4ff90079c0008abad00aab25031",
        to=phone_number,
        body=message,
        from_="HASHTAG",
    )
    logging.info(f"SMS sent to {phone_number}")
    return message



