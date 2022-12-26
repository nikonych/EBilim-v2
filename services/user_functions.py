from services.dbhandler import get_userx, update_transx
from services.parser import get_user_info, get_transkript2


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

async def get_trans_text(user_id):
    info = get_transkript2(user_id)
    text = ''
    total = 0
    count = 0
    gg = {}
    c = 1
    for k, v in info.items():
        v = v.replace(",", ".")
        pos = k[1].split(" ")
        pos[2] = "<code>" + str(100 - int(pos[2][:-1])) + "%</code>"
        text += '<b>{0}</b>\n {1}\n  Баллы: <code>{2}</code>\n\n'.format(k[0][:-7], " ".join(pos), v)
        total += float(v)
        count += 1
        gg[str(c)] = float(v)
        c += 1

    text += "Средний балл за семестр: <code>" + str(round(total / count, 2)) + "</code>"
    update_transx(user_id=user_id, f1=gg['1'],f2=gg['2'],f3=gg['3'],f4=gg['4'],f5=gg['5'],f6=gg['6'],f7=gg['7'])



    return text




