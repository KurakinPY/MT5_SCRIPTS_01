class MT5Session:
    server = "localhost:443"
    manager = "1000"
    password = "password"
    session = None
    connection = False

    def __init__(self, _server, _manager, _password):
        import requests
        import hashlib
        import secrets
        import urllib3
        urllib3.disable_warnings()

        self.server = _server
        self.manager = _manager
        self.password = _password
        self.session = requests.Session()

        url = 'https://' + self.server + '/api/auth/start?version=3091&agent=WebAPI&login=' + self.manager + \
              '&type=manager'
        try:
            # Подключение к WebAPI MT5
            result = self.session.get(url, verify=False)
            srv_rand = bytes.fromhex(result.json().get('srv_rand'))
            password = self.password.encode('utf-16le')
            password = hashlib.md5(password).digest()
            password = hashlib.md5(password + b'WebAPI').digest()
            srv_rand = hashlib.md5(password + srv_rand).hexdigest()
            cli_rand = hashlib.md5(secrets.token_hex(16).encode('utf-16le')).hexdigest()
            url = 'https://' + self.server + '/api/auth/answer?srv_rand_answer=' + srv_rand + '&cli_rand=' + cli_rand
            result = self.session.get(url, verify=False)
            self.connection = (result.status_code == 200)

            # Проверка соединения
            url = 'https://' + self.server + '/api/test/access'
            result = self.session.get(url, verify=False)
            self.connection = (result.status_code == 200)

            # Получение общей информации о сервере
            url = 'https://' + self.server + '/api/common/get'
            result = self.session.get(url, verify=False)
            self.common = result.json().get('answer')

            # Получение времени сервера
            url = 'https://' + self.server + '/api/time/server'
            result = self.session.get(url, verify=False)
            self.servertime = result.json().get('answer')['time']
        except Exception as ex:
            print(ex)
            self.session = None


class MT5Mysql:
    def __init__(self, _host, _port, _user, _password, _db_name, _sql):
        import pymysql
        self.result = ''
        try:
            # Подключение к базе данных MySQL
            self.connection = pymysql.connect(host=_host, port=int(_port), user=_user, password=_password,
                                              database=_db_name, cursorclass=pymysql.cursors.DictCursor)
            try:
                # Исполнение SQL запроса
                with self.connection.cursor() as cursor:
                    cursor.execute(_sql)
                    self.result = cursor.fetchall()
            except Exception as _ex:
                print(f"{_ex}\nSQL syntax error!")
            finally:
                # Закрытие соединения с MySQL
                self.connection.close()
        except Exception as _ex:
            print(f"{_ex}\nDB connection error!")


class MT5Gateway:
    count = 0
    gateway = []
    name = []
    login = []
    password = []
    connection = []
    enable = []
    server = ''
    session = None

    def __init__(self, _server, _session):
        import urllib3
        urllib3.disable_warnings()

        self.count = 0
        self.name = []
        self.gateway = []
        self.login = []
        self.password = []
        self.connection = []
        self.enable = []
        self.server = _server
        self.session = _session

        url = 'https://' + _server + '/api/gateway/total'
        try:
            result = _session.get(url, verify=False)
            self.count = int(result.json().get('answer')['total'])
        except Exception as ex:
            print(ex)

        for i in range(self.count):
            url = 'https://' + _server + '/api/gateway/next?index=' + str(i)
            try:
                result = _session.get(url, verify=False).json().get('answer')
                self.name.append(result['Name'])
                self.gateway.append(result['GatewayServer'])
                self.login.append(result['GatewayLogin'])
                self.password.append(result['GatewayPassword'])
                self.connection.append(bool(int(result['State']['SysConnection'])))
                self.enable.append(bool(int(result['Enable'])))
            except Exception as ex:
                print(ex)

    def restart(self):
        url = 'https://' + self.server + '/api/gateway/restart'
        try:
            result = self.session.get(url, verify=False)
            return result.status_code
        except Exception as ex:
            print(ex)


class MT5Feeder:
    count = 0
    feeder = []
    name = []
    login = []
    password = []
    connection = []
    enable = []
    server = ''
    session = None

    def __init__(self, _server, _session):
        import urllib3
        urllib3.disable_warnings()

        self.count = 0
        self.name = []
        self.feeder = []
        self.login = []
        self.password = []
        self.connection = []
        self.enable = []
        self.server = _server
        self.session = _session

        url = 'https://' + _server + '/api/feeder/total'
        try:
            result = _session.get(url, verify=False)
            self.count = int(result.json().get('answer')['total'])
        except Exception as ex:
            print(ex)

        for i in range(self.count):
            url = 'https://' + _server + '/api/feeder/next?index=' + str(i)
            try:
                result = _session.get(url, verify=False).json().get('answer')
                self.name.append(result['Feeder'])
                self.feeder.append(result['GatewayServer'])
                self.login.append(result['GatewayLogin'])
                self.password.append(result['GatewayPassword'])
                self.connection.append(bool(int(result['State']['SysConnection'])))
                self.enable.append(bool(int(result['Enable'])))
            except Exception as ex:
                print(ex)

    def restart(self):
        url = 'https://' + self.server + '/api/feeder/restart'
        try:
            result = self.session.get(url, verify=False)
            return result.status_code
        except Exception as ex:
            print(ex)


class MT5User:
    def __init__(self, _server, _session, _login):
        # urllib3.disable_warnings()
        self.user = {}
        self.login = _login
        self.server = _server
        self.session = _session
        url = 'https://' + _server + '/api/user/get?login=' + _login
        try:
            result = _session.get(url, verify=False)
            self.user = result.json()
        except Exception as ex:
            print(ex)

    def update_group(self, old, new):
        import json
        user_group = self.user['answer']['Group']
        user_group = user_group.replace(old, new, 1)
        self.user['answer']['Group'] = user_group
        self.user = json.dumps(self.user['answer'])
        url = 'https://' + self.server + '/api/user/update?'
        try:
            result = self.session.post(url, self.user)
            return result
        except Exception as ex:
            print(ex)

    def add_amount(self, action, amount, comment):
        url = 'https://' + self.server + '/api/trade/balance?login=' + self.login + '&type='+str(action) + \
              '&balance=' + str(amount) + '&comment=' + parse.quote(str(comment))
        try:
            result = self.session.get(url)
            if result.json().get('retcode') == '0 Done':
                return 0
            else:
                return -1
        except Exception as ex:
            print(ex)
