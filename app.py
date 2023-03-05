import telebot
from config import TOKEN, currency
from extensions import APIException, CurrencyConverter, ModAmount

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_instruction(message: telebot.types.Message):
    text = 'Для начала работы введите сообщение в следующем формате:\n \
<название исходной валюты> <название конечной валюты> <количество исходной валюты> \n \
Чтобы узнать доступные валюты введите команду /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def send_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key, ))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Введите команду или 3 параметра:\n \
<название исходной валюты> <название конечной валюты> <количество исходной валюты>\n \
Чтобы узнать доступные валюты введите команду /values ')

        quote, base, amount = values
        result = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Стоимость {ModAmount.mod_amount(amount)} {quote} = {result} {base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
