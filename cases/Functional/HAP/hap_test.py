from os import environ as env
import random
from Common import dbquery
from pytest_bdd import scenario, given, when, then
import requests
import json
import Common.auth as auth
import pytest

IP = env.get('HAP_URL')
FIRST_NAME = "maleksander" + str(random.randint(100, 999))
LAST_NAME = "maaazzz" + str(random.randint(100, 999))
ROLE = 'MANUAL_ENTRY'


@pytest.fixture(scope="module")
def post_request(get_token):
    def _send_post_request(data):
        url1 = f'{IP}{data.url}'
        type(data.params)
        headers = {'Accept': 'application/json;charset=UTF-8', 'Content-Type': 'application/json;charset=UTF-8'}
        req = requests.post(url1, data=data.params, headers=headers, auth=auth.BearerAuth(get_token))
        return req

    return _send_post_request


@pytest.fixture(scope="module")
def put_request(get_token):
    def _send_put_request(data):
        url1 = f'{IP}{data.url}'
        type(data.params)
        headers = {'Accept': 'application/json;charset=UTF-8', 'Content-Type': 'application/json;charset=UTF-8'}
        req = requests.put(url1, data=data.params, headers=headers, auth=auth.BearerAuth(get_token))
        return req

    return _send_put_request


@pytest.fixture
def create_person_403(post_request):
    def _send_create_person():
        data = auth.StdClass()
        card_data = auth.PersonData('00020001', '900003', FIRST_NAME, LAST_NAME)
        data.params = card_data.make_data()
        data.url = '/manual_entry/create_new_person'
        return post_request(data)

    return _send_create_person


@pytest.fixture
def create_new_card(create_person, post_request):
    def _send_new_card():
        resp = json.loads(create_person.text)
        data = auth.StdClass()
        person_data = auth.CardData(resp['personId'], resp['accountId'], '00020001', '900003', FIRST_NAME, LAST_NAME)
        data.params = person_data.make_data()
        data.url = '/manual_entry/create_new_card'
        return post_request(data)

    return _send_new_card


@pytest.fixture
def change_card_balance(create_person, post_request):
    def _send_change_card_balance():
        resp = json.loads(create_person.text)
        data = auth.StdClass()
        card_data = auth.CardBalance('200', resp['appId'], 'C')
        data.params = card_data.make_data()
        data.url = '/manual_entry/change_card_balance'
        return post_request(data)

    return _send_change_card_balance


@pytest.fixture
def search_card(create_person, post_request):
    def _send_search_card():
        resp = json.loads(create_person.text)
        data = auth.StdClass()
        search_data = auth.SearchCard(resp['appId'])
        data.params = search_data.make_data()
        data.url = '/cardholders/search'
        return post_request(data)

    return _send_search_card


@pytest.fixture
def limit_card(create_person, put_request):
    def _send_limit_card():
        resp = json.loads(create_person.text)
        data = auth.StdClass()
        app_id = resp['appId']
        limit_data = auth.CardLimitData(make_id_for_card(app_id), 'card', 'all', 100)
        data.params = limit_data.make_data()
        data.url = '/limit/daily'
        return put_request(data)
    return _send_limit_card


@pytest.fixture
def change_admin_role(post_request):
    def _send_change_admin_role():
        data = auth.StdClass()
        data.params = {
            "id": 27,
            "name": "POSTING_FULL"
        }
        json.dumps(data.params)
        data.url = '/admin/role/add/roleTemplateId/28'
        return post_request(data)
    return _send_change_admin_role


@pytest.fixture
def change_role():
    delete_role()
    yield
    add_role()


@pytest.fixture
def change_all_role():
    remove_all_roles()
    yield
    set_all_roles()


def make_id_for_card(app_id):
    query = dbquery.Dbquery.get_cardcode_by_app_id((app_id,))
    print(query[1].strftime("%Y-%m-%d"))
    return f'{query[0]}_{query[1].strftime("%Y-%m-%d")}'


def get_user_id():
    user_name = [env.get('HAP_LOGIN')]
    user_id = dbquery.Dbquery.get_user_id(user_name)
    return user_id[0]


def get_role_id():
    role_id = dbquery.Dbquery.get_role_id([ROLE])
    return role_id[0]


def delete_role():
    data = [get_user_id(), get_role_id()]
    dbquery.Dbquery.remove_role(data)


def add_role():
    data = [get_user_id(), get_role_id()]
    dbquery.Dbquery.add_role(data)


def remove_all_roles():
    data = [get_user_id(), get_role_id()]
    dbquery.Dbquery.remove_all_role_without(data)


def set_all_roles():
    results = dbquery.Dbquery.get_all_roles()
    user_id = (get_user_id(),)
    var = [user_id + x for x in results if x[0] != 50]
    dbquery.Dbquery.add_role_multi(var)


def test_manual_entry_0001(create_person_403, change_role):
    resp1 = create_person_403()
    assert resp1.status_code == 403


def test_manual_entry_0002(create_new_card, change_role):
    resp1 = create_new_card()
    assert resp1.status_code == 403


def test_manual_entry_0003(change_card_balance, change_role):
    resp1 = change_card_balance()
    assert resp1.status_code == 403


def test_manual_entry_0004(change_all_role, search_card):
    resp1 = search_card()
    assert resp1.status_code == 403


def test_manual_entry_0005(change_all_role, limit_card):
    resp1 = limit_card()
    assert resp1.status_code == 403


def test_manual_entry_0006(change_admin_role, change_all_role):
    resp1 = change_admin_role()
    assert resp1.status_code == 403
