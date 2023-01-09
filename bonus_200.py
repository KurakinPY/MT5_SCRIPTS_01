import os
import logging
import datetime
import time
from configparser import ConfigParser
import _mt5_webapi_lib as mt5
import _sql_requests as sql

# Загрузка конфигурации
config = ConfigParser()
config.read('config.ini')
DB_HOST = config.get('DATABASE', 'DB_HOST')
DB_PORT = config.get('DATABASE', 'DB_PORT')
DB_USER = config.get('DATABASE', 'DB_USER')
DB_PASSWORD = config.get('DATABASE', 'DB_PASSWORD')
DB_NAME = config.get('DATABASE', 'DB_NAME')
MT5_HOST = config.get('MT5', 'MT5_HOST')
MT5_USER = config.get('MT5', 'MT5_USER')
MT5_PASSWORD = config.get('MT5', 'MT5_PASSWORD')
ON_ITERATION = int(config.get('SLEEP', 'ON_ITERATION'))
ON_ERROR = int(config.get('SLEEP', 'ON_ERROR'))

# Создаем log файлы для скрипта
log_name = str('_mt5_bonus_compensation_' + str(datetime.date.today()) + '.log')
if os.path.exists(log_name):
    os.remove(log_name)
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)
logging.info(str(datetime.datetime.now()) + ' Script starting')
print("====================================================================")
print("* Скрипт списывает бонус 500$ при условии, что (Equity-Credit) < 200")
print("* и в истории есть вывод средств на любую сумму                     ")
print("====================================================================")
print(str(datetime.datetime.now()) + ' Script starting')

# Главный цикл
mt5_connection = -1
while True:
    try:
        if mt5_connection == -1:
            mt5_session = mt5.MT5Session(MT5_HOST, MT5_USER, MT5_PASSWORD)
            log_message = 'MT5 Connection - OK'
            logging.info(log_message)
            print(log_message)
            mt5_connection = 0

        # Вычитаем бонус в сумме 500$
        bonus_tag = '#Bonus200'
        from_date = '2022-09-01'
        to_date = '3000-09-01'
        action = 6

        accounts_list = mt5.MT5Mysql(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME,
                                     sql.sql_bonus_withdrawal_list(bonus_tag, from_date, to_date))

        if len(accounts_list.result) > 0:
            for item in accounts_list.result:
                account = mt5.MT5User(mt5_session.server, mt5_session.session, str(item['Login']))
                bonus = str(item['Bonus'])
                result = account.add_amount(action, -float(bonus), bonus_tag)
                if result == 0:
                    log_message = str(datetime.datetime.now()) + ' Login: ' + str(item['Login']) + ' Bonus out: -500'
                else:
                    log_message = str(datetime.datetime.now()) + ' Login: ' + str(item['Login']) + \
                                  ' Correction ERROR!'
                logging.info(log_message)
                print(log_message)
    except Exception as _ex:
        mt5_connection = -1
        print(_ex)
        logging.error(str(datetime.datetime.now()) + str(_ex))
        time.sleep(ON_ERROR)
    finally:
        time.sleep(ON_ITERATION)
        continue
