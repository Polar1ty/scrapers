import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id,
                     'Hi {0.first_name}, my name is {1.first_name}\n☂Input your city below👇👇👇\nIf you need help write "/help"'.format(
                         message.from_user,
                         bot.get_me()))


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Sry, but nobody here can help you :)')


@bot.message_handler(content_types=['text'])
def weather(message):
    try:
        city = message.text
        observation = config.owm.weather_at_place(city)
        w = observation.get_weather()
        temperature = w.get_temperature('celsius')['temp']
        wind = w.get_wind()['speed']
        humidity = w.get_humidity()
        status = w.get_detailed_status()
        bot.send_message(message.chat.id,
                         'Weather in {0} for now\nTemperature: {1}\nWind: {2}\nHumidity: {3}\nStatus: {4}'.format(city,
                                                                                                                  temperature,
                                                                                                                  wind,
                                                                                                                  humidity,
                                                                                                                  status))
    except:
        bot.send_message(message.chat.id, 'Something went wrong🙁\nTry to input another city')


# BOT RUNNING
if __name__ == '__main__':
    bot.infinity_polling()
