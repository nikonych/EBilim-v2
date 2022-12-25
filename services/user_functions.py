from services.dbhandler import get_userx
from services.parser import get_user_info


# Текст для профиля
async def get_profile_text(user_id):
    profile = get_user_info(user_id)
    user = get_userx(user_id)
    name = ""
    for i in profile[0]:
        name += i + " "
    text = f"Профиль: <code>{name}</code>\n" \
           f"Cтатус: <code>{user['status']}</code>\n\n" \
           f"Долг за обучение: <code>{profile[1]}</code>\n" \
           f"Бюджет/контракт: <code>{profile[2]}</code>\n" \
           f"Шифр оплаты: <code>{profile[3]}</code>\n\n" \
           f"Дата рождения: <code>{profile[4]}</code>\n" \
           f"ИНН: <code>{profile[5]}</code>\n" \
           f"Номер телефона: <code>{profile[7]}</code>\n\n"

    if user['payment'] is None:
        text += "Реквизиты: не указаны("
    else:
        text += f"Реквизиты: <code>{user['payment']}</code>"
    return text



