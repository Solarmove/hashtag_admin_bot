import logging
from typing import Literal

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiohttp import web

from bot.src.services.sms_mailing_service import send_sms
from bot.src.utils.unitofwork import UnitOfWork
import random
from string import ascii_letters, digits

async def generate_random_code():
    return "".join(random.choices(f"{ascii_letters}{digits}", k=5))


async def send_sms_handler(request: web.Request):
    uow: UnitOfWork = request.app["uow"]
    bot: Bot = request.app["bot"]
    body = await request.json()
    phone_numbers = body.get("phone_numbers", [])
    bar: Literal['hashtag', 'hashrest'] = body.get("bar", [])
    if not phone_numbers:
        return web.json_response(
            "Forbidden",
            status=403,
        )
    async with uow() as uow:
        for phone_number in phone_numbers:
            deep_link_exist = await uow.deep_link_repo.find_one(
                phone_numbers=phone_number,
                bar=bar,
            )
            if deep_link_exist:
                continue
            code = await generate_random_code()
            deep_link = await create_start_link(bot, f"sms_{code}_{bar}")
            await uow.deep_link_repo.add_one(
                {
                    "phone_number": phone_number,
                    "code": code,
                    'bar': bar,
                }
            )
            bar_title = "Hashtag Lounge Bar" if bar == "hashtag" else "Hash&Rest Lounge Bar"
            text = (
                f"Привіт!\n"
                f"Твій друг подарував тобі безкоштовний покур в {bar_title}.\n"
                f"Перейди за посиланням {deep_link}"
            )
            try:
                await send_sms(
                    phone_number, text
                )
            except Exception as ex:
                logging.error(ex)
                await uow.rollback()
                continue
            await uow.commit()


    return web.Response(
        status=201
    )
