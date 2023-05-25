import kanlib_mt5webapi_02 as mt5
import json

MT5_SERVER = '46.42.223.100:443'  # DEMO
MANGER_LOGIN = '1029'
MANGER_PASSWORD = 'dj805dktj85'

mt5_session = mt5.MT5Session(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD)
print(mt5_session.connection, mt5_session.servertime)

from_login = '2699'     # int(input())
to_login = '2697'       # int(input())

# url = 'https://' + MT5_SERVER + '/api/deal/get_page?login=' + from_login + \
#       '&from=0000000000&to=9999999999&offset=0&total=0'
# deals_result = mt5_session.session.get(url, verify=False)
# deals_answer = deals_result.json().get('answer')

# for deal in deals_answer:
#     deal['Login'] = to_login
#     deal['Comment'] = 'TEST_13'
#
# for deal in deals_answer:
#     deal = json.dumps(deal)
#     result = mt5_session.session.post('https://' + MT5_SERVER + '/api/deal/update', deal)
#     print(result.json(), deal)
#
#

# url = 'https://' + MT5_SERVER + '/api/deal/get_page?login=' + from_login + \
#       '&from=0000000000&to=9999999999&offset=0&total=0'
# deals_result = mt5_session.session.get(url, verify=False)
# deals_answer = deals_result.json().get('answer')

url = 'https://' + MT5_SERVER + '/api/history/get_page?login=' + from_login + \
      '&from=0000000000&to=9999999999&offset=0&total=0'
orders_result = mt5_session.session.get(url, verify=False)
orders_answer = orders_result.json().get('answer')


for order in orders_answer:
    order['Login'] = to_login
    order['Comment'] = 'TEST_13'

for order in orders_answer:
    order = json.dumps(order)
    print(order)
    result = mt5_session.session.post('https://' + MT5_SERVER + '/api/history/update', order)
    print(result.json(), order)


