def mt5_connect(server, manager, password):
    # Устанавливаем постоянно HTTPS соединение с MT5 WebAPI по менеджерскому логину
    # Возвращает requests.Session() или код ответа сервера status_code

    import requests
    import hashlib
    import secrets

    # Создаем сессию и отправляем первый запрос
    session = requests.Session()
    request_str = 'https://' + server + '/api/auth/start?version=3091&agent=WebAPI&login=' + manager + '&type=manager'
    request_result = session.get(request_str, verify=False)
    srv_rand = bytes.fromhex(request_result.json().get('srv_rand'))
    # Ответ сервера сохранен в srv_rand в виде байт-кода

    # Хеширование ответа серверу по правилам MT5
    password = password.encode('utf-16le')
    password = hashlib.md5(password).digest()
    password = hashlib.md5(password + b'WebAPI').digest()
    srv_rand = hashlib.md5(password + srv_rand).hexdigest()
    cli_rand = hashlib.md5(secrets.token_hex(16).encode('utf-16le')).hexdigest()
    # Ответ хэширован в srv_rand и cli_rand

    # Отправка ответа серверу MT5
    request_str = 'https://' + server + '/api/auth/answer?srv_rand_answer=' + srv_rand + '&cli_rand=' + cli_rand
    request_result = session.get(request_str, verify=False)

    if request_result.status_code == 200:
        return session
    else:
        return request_result.status_code


def get_gateway_status(server, manager, password, gate_index):
    result = 0
    # Открываем соединение с MT5 и получаем список символов
    # '/api/gateway/next?index=0' - Получение шлюза по индексу
    try:
        session = mt5_connect(server, manager, password)
        gateway_config = session.get('https://' + server + '/api/gateway/next?index=' + str(gate_index))
        result = int(gateway_config.json().get('answer')['State']['BytesReceived'])
    except Exception as ex:
        print(f"{ex}\nERROR MT5 Server no connection!")
    finally:
        return result
