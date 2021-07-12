from os import environ as env
import pytest
import requests
import json
import random
from hashlib import md5
import Common.auth as auth

FIRST_NAME = "maleksander" + str(random.randint(100, 999))
LAST_NAME = "maaazzz" + str(random.randint(100, 999))


@pytest.fixture(scope="module")
def get_token():
    IP = env.get('HAP_URL')
    LOGIN = env.get('HAP_LOGIN')
    PASSWORD = env.get('HAP_PASSWORD').encode('utf-8')
    hash = md5(PASSWORD).hexdigest()
    url = f'{IP}/login'
    payload = {'username': LOGIN, 'password': hash}
    response = requests.get(url, params=payload)
    assert response.status_code == 200
    data = json.loads(response.text)
    token = data['token']
    print('get token')
    return token


@pytest.fixture(scope="module")
def create_person(post_request):
    data = auth.StdClass()
    card_data = auth.PersonData('00020001', '900003', FIRST_NAME, LAST_NAME)
    data.params = card_data.make_data()
    data.url = '/manual_entry/create_new_person'
    return post_request(data)
