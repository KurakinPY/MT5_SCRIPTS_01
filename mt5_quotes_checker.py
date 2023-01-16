"""
Anton Kurakin, [05.08.2022 11:13]
mt5_tass_admin
BotFather, [05.08.2022 11:13]
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
Anton Kurakin, [05.08.2022 11:15]
mt5_tass_admin_bot
BotFather, [05.08.2022 11:15]
Done! Congratulations on your new bot. You will find it at t.me/mt5_tass_admin_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
Use this token to access the HTTP API:
5423258967:AAG5CsaNQB9bY3JEHMkbKq5A2clYIs2n08Q
Keep your token secure and store it safely, it can be used by anyone to control your bot.
For a description of the Bot API, see this page: https://core.telegram.org/bots/api
telegram_send: 64438
"""

import time
import logging
import urllib3
import datetime
import telegram_send
import _quotes_checker as qch
'''=================================================================================================================='''
# MT5_SERVER = '109.169.85.16:443'
MT5_SERVER = 'localhost:443'
MANGER_LOGIN = '1029'
MANGER_PASSWORD = 'dj805dktj85'
urllib3.disable_warnings()

logging.basicConfig(filename='mt5_quotes_checker.log', encoding='utf-8', level=logging.INFO)
logging.info(str(datetime.datetime.now()) + ' - Checker started')
telegram_send.send(messages=[str(datetime.datetime.now()) + ' - Gateway checker started!'])

try:
    print('==============================================================================')
    print('QUOTES CHECKER MT5 REAL')
    print("Script started at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print('==============================================================================')

    while True:
        if qch.get_gateway_status(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD, 0) == 0:
            logging.error(str(datetime.datetime.now()) + ' - Gateway ERROR')
            telegram_send.send(messages=[str(datetime.datetime.now()) + ' - Gateway ERROR'])
            print(datetime.datetime.now(), 'Gateway ERROR')
        else:
            print(datetime.datetime.now(), 'OK')
        time.sleep(60)
except Exception as ex:
    logging.error(f"{ex}\n" + str(datetime.datetime.now()) + " - Script ERROR")
finally:
    logging.info(str(datetime.datetime.now()) + ' - Gateway checker stopped!')
    telegram_send.send(messages=[str(datetime.datetime.now()) + ' - Gateway checker stopped!'])



