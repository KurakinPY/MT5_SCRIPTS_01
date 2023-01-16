"""
====================================================================================
 Скрипт проверяет следующие параметры MT5:
 1. Статус соединения с Asses Servers
 2. Статус соединения с Gateways
 3. Статус соединения с Feeders

 Канал mt5_tass_admin https://t.me/+VHEULnIQjeVlYjRi
 Канал mt5_tass_warning ID: -1001504889164
 token = "5423258967:AAG5CsaNQB9bY3JEHMkbKq5A2clYIs2n08Q"
 channel_id = "-1001504889164"
====================================================================================
"""
import time
import datetime
import urllib3
import telebot
import _mt5_webapi_lib as mt5

# MT5_SERVER = '109.169.85.16:443'  # Real
MT5_SERVER = '62.173.147.150:443'  # Dev
# MT5_SERVER = 'localhost:443'
MANGER_LOGIN = '1029'
MANGER_PASSWORD = 'dj805dktj85'
TOKEN = ''
CHANNEL_ID = ''
# TOKEN = "5423258967:AAG5CsaNQB9bY3JEHMkbKq5A2clYIs2n08Q"
# CHANNEL_ID = "-1001504889164"
urllib3.disable_warnings()


def time_now():
    result = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return result


def send_message(message, token, channel_id, sleep):
    message = time_now() + ' ' + message
    print(message)
    if token != '' and channel_id != '':
        telegram_bot = telebot.TeleBot(TOKEN)
        telegram_bot.send_message(CHANNEL_ID, message)
    time.sleep(sleep)


def check_quotes_connection(quotes):
    result = False
    if quotes.count > 0:
        print('==================================================')
        for i in range(quotes.count):
            print(time_now(), quotes.name[i], ' - Enable:', quotes.enable[i], '/ Connection:', quotes.connection[i], )
            if not quotes.connection[i]:
                quotes.restart()
                send_message(quotes.name[i] + ' RESTART', '', '', 0)
            elif quotes.enable[i] and quotes.connection[i]:
                result = True
    return result


def main():
    try:
        send_message('Skript running', TOKEN, CHANNEL_ID, 0)
        while True:
            # Проверяем соединение с MT5 и создаем сессию, если False, то повторяем проверку
            mt5_session = mt5.MT5Session(MT5_SERVER, '1029', 'dj805dktj85')
            if not mt5_session.connection:
                send_message('MT5 connection ERROR!!!', TOKEN, CHANNEL_ID, 30)
                continue

            # Ищем хоть один работающий Gateway, если False, перезагружаем Gateways (две попытки), иначе ERROR
            mt5_gateway = mt5.MT5Gateway(mt5_session.server, mt5_session.session)
            gateway_connection = check_quotes_connection(mt5_gateway)

            # Ищем хоть один работающий Feeder, если False, перезагружаем Feeder (две попытки), иначе ERROR
            mt5_feeder = mt5.MT5Feeder(mt5_session.server, mt5_session.session)
            feeder_connection = check_quotes_connection(mt5_feeder)

            # Если NOT Gateways and NOT Feeders, то сообщение в Telegram
            if (not gateway_connection) and (not feeder_connection):
                send_message('Gateway and Feeder ERROR!!!', TOKEN, CHANNEL_ID, 0)
                continue
            send_message('MT5 Ok', '', '', 30)
    except Exception as ex:
        send_message(str(ex), TOKEN, CHANNEL_ID, 0)
        print(ex)


if __name__ == '__main__':
    main()
