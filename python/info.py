import json


def __load_data():
    f = open('../txt/.info', 'r')
    data = f.read()
    f.close()
    return json.loads(data)


def get_token():
    data = __load_data()
    return data.get('token')


def get_invite_url():
    data = __load_data()
    return data.get('invite_url')


def get_client_id():
    data = __load_data()
    return data.get('client_id')


def get_creator_id():
    data = __load_data()
    return data.get('creator_id')
