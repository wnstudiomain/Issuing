from os import environ as env
import random

from pytest_bdd import scenario, given, when, then
import requests
import json
import Common.auth as auth
import pytest

IP = env.get('HAP_URL')
ISSUING_DATA = {
    "issuingData": {
        "accountId": "",
        "appId": "",
        "deliveryAddress": {
            "address": "street?build?flat_office",
            "city": "Kursk",
            "country": "643",
            "mailFirstName": "maleksander" + str(random.randint(10, 99)),
            "mailLastName": "maaazzz" + str(random.randint(10, 99)),
            "state": "KurskState",
            "zipCode": "305005"
        },
        "personId": "",
        "productId": "900003",
        "urgencyIssuing": 1,
        "welcomePack": 1
    },
    "sign": "",
}
CONTACT_DATA = {
    "contact": {
        "email": "maaazzz@mail.ru",
        "phone": "+790452749999"
    },
}
ID_DATA = {
    "identificator": {
        "agentIdentificator": "00020001",
        "rid": ""
    },
}


@pytest.fixture(scope="module")
def post_request(get_token):
    def _send_post_request(data):
        url1 = f'{IP}{data.url}'
        type(data.params)
        headers = {'Accept': 'application/json;charset=UTF-8', 'Content-Type': 'application/json;charset=UTF-8'}
        req = requests.post(url1, data=data.params, headers=headers, auth=auth.BearerAuth(get_token))
        # print(response.url)
        return req

    return _send_post_request


@pytest.fixture(scope="module")
def create_person(post_request):
    def _send_create_person():
        data = auth.StdClass()
        data.params = json.dumps({
            "address": {
                "address": "street?build?flat_office",
                "city": "Kursk",
                "country": "643",
                "mailFirstName": "maleksander",
                "mailLastName": "maaazzz",
                "zipCode": "305005"
            },
            "person": {
                "contactCode": "apitest",
                "dateOfBirthday": "1990-03-23",
                "firstName": "aleksander",
                "lastName": "aaazzz",
                "middleName": "{{$randomAbbreviation}}",
                "nationality": "643",
                "passportId": "3809100100"
            },
            **ISSUING_DATA,
            **CONTACT_DATA,
            **ID_DATA
        })
        data.url = '/manual_entry/create_new_person'
        return post_request(data)

    return _send_create_person


def create_new_card(create_person, post_request):
    resp = json.loads(create_person.text);
    data = auth.StdClass()
    ISSUING_DATA['issuingData']['accountId'] = resp['accountId']
    ISSUING_DATA['issuingData']['personId'] = resp['personId']
    data.params = json.dumps({
        **ISSUING_DATA,
        **CONTACT_DATA,
        **ID_DATA
    })
    # print(ISSUING_DATA)
    data.url = '/manual_entry/create_new_card'
    return post_request(data)


@pytest.fixture(scope="module")
def change_card_balance(create_person, post_request):
    def _send_change_card_balance(data):
        data.url = '/manual_entry/change_card_balance'
        return post_request(data)

    return _send_change_card_balance


def test_manual_entry_0001(create_person):
    resp1 = create_person()
    assert resp1.status_code == 200
    resp = json.loads(resp1.text)
    print(resp)


def test_manual_entry_0002(create_new_card):
    assert create_new_card.status_code == 200
    resp = json.loads(create_new_card.text)
    print("\n")
    print(resp)


def test_manual_entry_0003(create_person, change_card_balance):
    resp1 = create_person()
    resp = json.loads(resp1.text)
    data = auth.StdClass()
    card_data = auth.CardBalance('200', resp['appId'], 'C')
    data.params = card_data.make_data()
    resp2 = change_card_balance(data)
    assert resp2.status_code == 200
    resp = json.loads(resp2.text)
    print(resp)
