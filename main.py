"""import copy


def step(i, j, a):
    temp = a.copy()
    for k in range(len(temp[0])):
        temp[i][k] ^= 1
        temp[k][j] ^= 1
    temp[i][j] ^= 1
    return temp


def rec(a, depth, cmd, rr):
    if depth < 10:
        temp = 0
        for ii in a:
            temp += sum(ii)
        if temp == 0:
            return True
        else:
            for ii in range(rr, len(a[0])):
                for jj in range(len(a[0])):
                    if [ii, jj] not in cmd:
                        temp = copy.deepcopy(a)
                        for k in range(len(temp[0])):
                            temp[ii][k] ^= 1
                            temp[k][jj] ^= 1
                        temp[ii][jj] ^= 1
                        if rec(temp, depth + 1, cmd + [[ii, jj]], ii):
                            print(ii, jj)
                            return True
    return False


for _ in range(int(input())):
    n = int(input())
    a = []
    for i in range(n):
        a.append(list(map(int, input().split())))
    rec(a, 0, [[]], 0)
"""

import telebot
from telebot import types

bot = telebot.TeleBot("")

"""menu = types.InlineKeyboardMarkup(row_width=3)
menu.add(
    types.InlineKeyboardButton(text='Hi!', callback_data='b1'),
    types.InlineKeyboardButton(text='Hello!', callback_data='b2')
)
bot.send_message(message.chat.id, 'text', reply_markup=menu)
"""

users = {}
# tg-name: chat_id, role, step, subjects
# step: reg -> role -> subject


def data_import():
    with open("roles.txt", "r") as f:
        for i in f.readlines():
            temp = i.split()
            if temp != ["\n"]:
                users[temp[0]] = [int(temp[1]), temp[2], int(temp[3]), temp[4:]]


def data_export():
    with open("roles.txt", "w") as f:
        for i in users:
            f.write("{} {} {} {} {}\n".format(i, str(users[i][0]), str(users[i][1]), str(users[i][2]), " ".join(users[i][3])))


def mark(color):
    if color == "green":
        return "\033[42mLOG\033[0m   "
    elif color == "yellow":
        return "\033[43mLOG\033[0m   "
    elif color == "red":
        return "\033[41mLOG\033[0m   "


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.from_user.username == "None":
        bot.send_message(message.chat.id, 'Привет\nУ тебя нет имени в TG, проверь'
                                          'настройки!\nПосле заново отправь команду /start')
    else:
        if message.from_user.username not in users:
            users[message.from_user.username] = [message.chat.id, "none", 0, ["Не указано"]]
            data_export()
            print(mark("green") + "Новый пользователь:", message.chat.id, message.from_user.username)
            main(message, "Привет, {}!".format(message.from_user.username))


@bot.message_handler(commands=['back'])
def main(message, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Список наставников")
    markup.add(item1)
    if users[message.from_user.username][1] == "Наставник":
        item2 = types.KeyboardButton("Предметы")
        markup.add(item2)
        item3 = types.KeyboardButton("Удалиться")
    else:
        item3 = types.KeyboardButton("Стать наставником")
    markup.add(item3)
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Список наставников":
        temp = "Вот наши наставники:\n"
        for i in users:
            if users[i][1] == "Наставник":
                temp += str(i) + " | " + " ".join(users[i][3]) + "\n"
        main(message, temp)
    elif message.text == "Предметы":
        if users[message.from_user.username][1] == "Наставник":
            users[message.from_user.username][2] = 1
            bot.send_message(message.chat.id, "Напиши предметы через пробел, с которыми ты можешь помочь")
        else:
            users[message.from_user.username][2] = 1
            bot.send_message(message.chat.id, "Напиши предметы через пробел, которые тебе интересны")
    elif message.text == "Удалиться":
        users[message.from_user.username][1] = "Удален"
        main(message, "Сделано, не забудь изменить предметы, которыми ты интересуешься")
        data_export()
    elif message.text == "Стать наставником":
        users[message.from_user.username][1] = "Наставник"
        main(message, "Сделано, не забудь изменить предметы, с которыми ты можешь помочь")
        data_export()
    else:
        if users[message.from_user.username][2] == 1:
            users[message.from_user.username][3] = message.text.split()
            main(message, "Принято")
        users[message.from_user.username][2] = 0
        data_export()


if __name__ == "__main__":
    print(mark("green") + "ROLES BOT")
    print(mark("yellow") + "Data importing...", end=" ")
    data_import()
    print("Completed")
    print(mark("yellow") + "Bot online!")
    print(users)
    bot.infinity_polling()
