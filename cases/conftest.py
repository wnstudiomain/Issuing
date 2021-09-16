from Common import ConstantNL4 as Card4
from Common import ConstantNL3 as Card3
from os import environ as env
from Common import auth
from Common import card_api
from faker import Faker
import pytest
import json
from hashlib import md5
from Common.client import APIClient
import allure

headers = {"Content-type": "application/json; charset=UTF-8"}
fake = Faker()

FIRST_NAME = fake.first_name()
LAST_NAME = fake.last_name()


@pytest.fixture(scope="class")
def card_env():
    if env.get('ENV') == 'nl4':
        return {
            'card1': Card4.ConstantNL4.CARD_9003,
            'card2': Card4.ConstantNL4.CARD_6807,
            'card3': Card4.ConstantNL4.CARD_6286,
            'card4': Card4.ConstantNL4.CARD_8712
        }
    else:
        return {
            'card3': Card3.ConstantNL3.CARD_1196,
            'card2': Card3.ConstantNL3.CARD_2814,
            'card4': Card3.ConstantNL3.CARD_2005
        }


@pytest.fixture(scope="module")
def api_client():
    ip = env.get('HAP_URL')
    return APIClient(ip)


@pytest.fixture(scope="module")
def get_token(api_client):
    login = env.get('HAP_LOGIN')
    password = env.get('HAP_PASSWORD').encode('utf-8')
    hash = md5(password).hexdigest()
    resp = api_client.get(path='login',
                          params={'username': login, 'password': hash})
    assert resp.status_code == 200
    data = json.loads(resp.text)
    token = data['token']
    print('get token')
    with allure.step('Сгенерировали токен авторизации'):
        return token


@pytest.fixture(scope="module")
def create_person(api_client, get_token):
    card_data = card_api.PersonData('00020001', '900003', FIRST_NAME, LAST_NAME)
    resp = api_client.post(path='manual_entry/create_new_person',
                           headers=headers,
                           json=card_data.make_data(),
                           auth=auth.BearerAuth(get_token))
    print(json.dumps(json.loads(resp.text), sort_keys=True, indent=4))
    with allure.step('Создали нового персона'):
        return resp
