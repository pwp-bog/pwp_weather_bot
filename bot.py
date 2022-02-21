import string
import telebot
from telebot import types

from config import TOKEN

from pyowm import OWM
from pyowm.utils.config import get_default_config

bot = telebot.TeleBot(TOKEN)

tmp = {}


# Объявление кнопок:
buttons = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button_locate = types.KeyboardButton("🌃  -  Выберите город")
button_info = types.KeyboardButton("🆘  -  Помощь")
button_weather = types.KeyboardButton("☀️  -  Узнать погоду")
button_author_info = types.KeyboardButton("🧑🏻‍💻  -  Об Авторе")
buttons.add(button_locate, button_info, button_weather, button_author_info)


# Обработчик команды start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, f"Привет  👋, я бот 🤖 который поможет узнать какая погода за окном  ⛅️. Если тебе будет что-то не понятно, ты всегда можешь воспользоваться кнопкой   \"🆘   -   Помощь\".  Удачного использования)", reply_markup=buttons
    )


# Обработчик текста который получает бот
@bot.message_handler(content_types=['text'])
def weather_handler(message):
    if message.text == "🧑🏻‍💻  -  Об Авторе":
        bot.send_message(
            message.chat.id, '''
🧑🏻‍💻  -  Автор: @pwp_programer
🐙  -  GitHub: https://github.com/pwp-programer
💸  -  Донаты: 4890 4947 9688 0706
        ''')

    if message.text == "🌃  -  Выберите город":
        tmp[message.chat.id] = []
        bot.send_message(
            message.chat.id, "__",
            reply_markup=(types.ReplyKeyboardRemove())
        )
        bot.register_next_step_handler(message, city)

    if message.text == "🆘  -  Помощь":
        bot.send_message(
            message.chat.id,
            '''
Если вы нажали, на эту кнопку, то вам необходима помощь. Я постараюсь вам помочь, если вы не смогли найти ответ на свой вопрос, напишите мне @pwp_programer

1.   🤖  -  Как пользоваться ботом?
    Для начала вам нужно выбрать город или страну в которой
    вы хотите узнать погоду. Для этого нужно нажать на
    соответствующую кнопку и ввести выбранное вами место.

    Далее вам нужно нажать на кнопку "Узнать погоду", для того
    что бы узнать погоду в выбранной вами местности.

2.  ❓  -  Зачем нужен этот бот?
    Данный бот был разработан в процессе изучения python и
    telebot. Автор не имеет какой-либо цели по дальнейшей
    монетизации и продвижению бота. Дальнейшая судьба бота
    не известна.

3.  📵  -  Решение проблем.
    Если вы столкнулись с какой-либо проблемой, то вам
    необходимо выполнить следующие действия:
        1. Сделать снимок экрана или его запись, где будет показана
        ваша проблема.

        2. Отправьте мне @pwp_programer, данный файл и подробно
        распишите в чём заключается проблема и какие действия
        к ней приводят.

        3. Проявите немного терпения и подождите пока ваша
        проблема не будет исправлена.

🤖  -  Bot ver 1.0
            ''')

    if message.text == "☀️  -  Узнать погоду":
        # !FIXME нажатие кнопки без ввода локации
        if tmp[message.chat.id]:
            # FIXME добавить возможность просматривать погоду на неделю
            config_dict = get_default_config()
            config_dict['language'] = 'ru'  # Локализация получаемых данных

            # Заносим в переменную текст из сообщения(пока он пустой)
            place = tmp[message.chat.id][0]
            # Токен для работы сервиса погоды
            owm = OWM('32fadfddbc16c9c16e64a4cdf27d9502', config_dict)
            mgr = owm.weather_manager()

            # Отправка запроса на сервер и обработка полученных данных
            try:
                observation = mgr.weather_at_place(place)

                w = observation.weather

                t = w.temperature("celsius")
                t1 = t['temp']
                t2 = t['feels_like']
                t3 = t['temp_max']
                t4 = t['temp_min']

                wi = w.wind()['speed']
                humi = w.humidity
                cl = w.clouds
                dt = w.detailed_status
                ti = w.reference_time('iso')
                pr = w.pressure['press']
                vd = w.visibility_distance

                bot.send_message(
                    message.chat.id,
                    "🌃  -  В городе: " + str(place) + "\n🌡 -  Температура: " + str(t1) + " °C" + "\n" +
                    "📈  -  Максимальная температура: " + str(t3) + " °C" + "\n" +
                    "📉  -  Минимальная температура: " + str(t4) + " °C" + "\n" +
                    "🧍‍♂️  -  Ощущается как: " + str(t2) + " °C" + "\n" +
                    "💨  -  Скорость ветра: " + str(wi) + " м/с" + "\n" +
                    "📡  -  Давление: " + str(pr) + " мм.рт.ст" + "\n" +
                    "💦  -  Влажность: " + str(humi) + " %" + "\n" +
                    "👀  -  Видимость: " + str(vd) + "  метров" + "\n" +
                    "📖  -  Описание: " + str(dt))
            except:
                bot.send_message(
                    message.chat.id, "Такого места нет в списке, попробуйте снова...")

        else:
            bot.send_message(message.chat.id, "Вы ещё не выбрали город")


def city(message: string) -> string:
    """[Считывание локации для определения погоды]

    Args:
        message ([type]): [description]
    """
    # Функция для считывания города или места
    tmp[message.chat.id] = []
    tmp[message.chat.id].append(message.text)
    print(tmp)
    bot.send_message(
        message.chat.id, f"Вы выбрали город: {tmp[message.chat.id][0]}", reply_markup=buttons)


if __name__ == '__main__':
    bot.polling(none_stop=True)
