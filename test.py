import kanlib_mt5webapi_02 as mt5
import json

# 1512 / Qwe123456
# 1168 / Qwe123456
# 1028 / Qwe123456
# 1029 / Qwe123456


# MT5_SERVER = '46.42.223.100:443'  # DEMO
MT5_SERVER = '109.169.85.16:443'  # REAL
MANGER_LOGIN = '1029'
# MANGER_LOGIN = '1029'
# MANGER_LOGIN = '1029'
# MANGER_PASSWORD = 'dj805dktj85'
MANGER_PASSWORD = 'Qwe123456'

mt5_session = mt5.MT5Session(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD)
print(mt5_session.connection, mt5_session.servertime)

url = 'https://' + MT5_SERVER + '/api/deal/get_page?login=' + '1425' + \
      '&from=0000000000&to=9999999999&offset=0&total=0'

url = 'https://' + MT5_SERVER + '/api/user/get?login=1425'
result = mt5_session.session.get(url, verify=False)
answer = result.json().get('answer')
print(answer)

