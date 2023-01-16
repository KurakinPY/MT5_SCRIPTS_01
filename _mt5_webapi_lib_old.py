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
        except Exception as ex:
            print(ex)
            self.session = None


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
