from aiogram.utils.link import create_tg_link


async def get_user_url(username: str | None, user_id: int, full_name: str):
    """Получает ссылку на пользователя"""
    if username:
        return f"@{username}"
    user_url = create_tg_link("user", id=user_id)
    return f"<a href='{user_url}'>{full_name}</a>"


async def add_user(user_id: int, username: str | None, full_name: str, uow: UnitOfWork):
    """Добавляет пользователя в базу данных"""

    user_exist = await uow.user_repo.find_one(id=user_id)
    if not user_exist:
        await uow.user_repo.add_one(
            {
                "id": user_id,
                "username": username,
                "full_name": full_name,
            }
        )
        await uow.commit()
