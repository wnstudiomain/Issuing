from Common import ConstantNL4 as Card4
from Common import ConstantNL3 as Card3
from os import environ as env
from faker import Faker
from os import path
from Common import dbquery
from Common import card_api
import requests
import json
import Common.auth as auth
import pytest
import allure
from Common import ConstantNL4 as Card
from Common.parser import ParseXLSX
from Common import trans
import datetime

from cases.conftest import card_env

headers = {"Content-type": "application/json; charset=UTF-8"}
IP = env.get('HAP_URL')
fake = Faker()
FIRST_NAME = fake.first_name()
LAST_NAME = fake.last_name()
ROLE = 'MANUAL_ENTRY'
FEATURE = 'Проверка HAP методов'
card17 = Card.ConstantNL4.CARD_6807
card1 = Card.ConstantNL4.CARD_9003
card2 = Card.ConstantNL4.CARD_6286
from_date = '2021-04-30'
to_date = '2021-04-30'
test_dir = path.dirname(path.abspath(__file__))
arn = ' -'
rrn = '112010000794'
arn1 = '74570001053705301554129'
rrn1 = '112009000739'
cards = {}


@pytest.fixture
def create_person_403(api_client, get_token):
    card_data = card_api.PersonData('00020001', '900003', FIRST_NAME, LAST_NAME)
    response = api_client.post(path='manual_entry/create_new_person',
                               headers=headers,
                               json=card_data.make_data(),
                               auth=auth.BearerAuth(get_token))
    with allure.step('Отправили запрос на создание нового пользователя'):
        return response


@pytest.fixture
def create_new_card(create_person, api_client, get_token):
    resp = json.loads(create_person.text)
    card_data = card_api.CardData(resp['personId'], resp['accountId'], '00020001', '900003', FIRST_NAME, LAST_NAME)
    response = api_client.post(path='manual_entry/create_new_card',
                               headers=headers,
                               json=card_data.make_data(),
                               auth=auth.BearerAuth(get_token))
    with allure.step('Отправили запрос на создание новой карты'):
        return response


def create_new_card_manual(api_client, get_token, person_id, account_id):
    card_data = card_api.CardData(person_id, account_id, '00020001', '900003', FIRST_NAME, LAST_NAME)
    response = api_client.post(path='manual_entry/create_new_card',
                               headers=headers,
                               json=card_data.make_data(),
                               auth=auth.BearerAuth(get_token))
    return response


@pytest.fixture
def change_card_balance(create_person, api_client, get_token):
    resp = json.loads(create_person.text)
    card_data = card_api.CardBalance('500', resp['appId'], 'C')
    response = api_client.post(path='manual_entry/change_card_balance',
                               headers=headers,
                               json=card_data.make_data(),
                               auth=auth.BearerAuth(get_token))
    with allure.step('Отправили запрос на пополнение карты'):
        return response


@pytest.fixture
def search_card(create_person, api_client, get_token):
    resp = json.loads(create_person.text)
    search_data = auth.SearchCard(resp['appId'])
    response = api_client.post(path='cardholders/search',
                               headers=headers,
                               json=search_data.make_data(),
                               auth=auth.BearerAuth(get_token))
    with allure.step('Отправили запрос на поиск карты'):
        return response


@pytest.fixture
def limit_card(create_person, api_client, get_token):
    def _send_limit_card(data):
        resp = json.loads(create_person.text)
        app_id = resp['appId']
        limit_data = auth.CardLimitData(make_id_for_card(app_id), data.limit_type, data.operation_type, data.value)
        data.params = limit_data.make_data()
        response = api_client.put(path=data.url,
                                  headers=headers,
                                  json=limit_data.make_data(),
                                  auth=auth.BearerAuth(get_token))
        with allure.step('Отправили запрос на изменение лимитов'):
            return response

    return _send_limit_card


@pytest.fixture
def change_admin_role(api_client, get_token):
    data = auth.StdClass()
    data.params = {
        "id": 27,
        "name": "POSTING_FULL"
    }
    response = api_client.post(path='admin/role/add/roleTemplateId/28',
                               headers=headers,
                               json=data.params,
                               auth=auth.BearerAuth(get_token))
    with allure.step('Отправили запрос на изменение роли'):
        return response


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


@pytest.fixture
def generate_statement_report(api_client, get_token):
    def _return_report(data):
        response = api_client.get(path='reports/transactions/card',
                                  params=data,
                                  auth=auth.BearerAuth(get_token))
        with allure.step('Отправили запрос на генерацию отчета'):
            return response

    return _return_report


def get_card_code(app_id):
    return dbquery.Dbquery.get_cardcode_by_app_id((app_id,))


def convert_card_code(query):
    return f'{query[0]}_{query[1].strftime("%Y-%m-%d")}'


def make_id_for_card(app_id):
    query = get_card_code(app_id)
    return convert_card_code(query)


def get_user_id():
    user_name = [env.get('HAP_LOGIN')]
    user_id = dbquery.Dbquery.get_user_id(user_name)
    with allure.step('Нашли id пользователя {} в БД'.format(user_name)):
        return user_id[0]


def get_role_id():
    role_id = dbquery.Dbquery.get_role_id([ROLE])
    with allure.step('Нашли id роли {} в БД'.format(ROLE)):
        return role_id[0]


def delete_role():
    user_name = env.get('HAP_LOGIN')
    data = [get_user_id(), get_role_id()]
    with allure.step('Удалили у пользователя {} роль {}'.format(user_name, ROLE)):
        dbquery.Dbquery.remove_role(data)


def add_role():
    user_name = env.get('HAP_LOGIN')
    data = [get_user_id(), get_role_id()]
    with allure.step('Вернули пользователяю {} роль {}'.format(user_name, ROLE)):
        dbquery.Dbquery.add_role(data)


def remove_all_roles():
    data = [get_user_id(), get_role_id()]
    dbquery.Dbquery.remove_all_role_without(data)


def set_all_roles():
    results = dbquery.Dbquery.get_all_roles()
    user_id = (get_user_id(),)
    var = [user_id + x for x in results if x[0] != 50]
    dbquery.Dbquery.add_role_multi(var)


def get_card_limit(app_id):
    query = dbquery.Dbquery.get_cardcode_by_app_id((app_id,))
    limit_arr = dbquery.Dbquery.get_card_limit((query[0], query[1].strftime("%Y-%m-%d")))
    return limit_arr


def get_arn(seqno):
    if seqno:
        seqno_d = seqno.split(':')
        seqno_for_query = dbquery.Dbquery.get_arn(seqno_d)
        return seqno_for_query
    else:
        pass


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод manual_entry/create_new_person')
def test_manual_entry_0001(change_role, create_person_403):
    with allure.step('Пользователь не создался, так как нет роли {}'.format(ROLE)):
        assert create_person_403.status_code == 403


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод manual_entry/create_new_card')
def test_manual_entry_0002(change_role, create_new_card):
    with allure.step('Карта не создалась, так как нет роли {}'.format(ROLE)):
        assert create_new_card.status_code == 403


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод manual_entry/change_card_balance')
def test_manual_entry_0003(change_role, change_card_balance):
    with allure.step('Баланс карты не поплнен, так как нет роли {}'.format(ROLE)):
        assert change_card_balance.status_code == 403


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод manual_entry/create_new_person')
def test_manual_entry_0004(create_person):
    with allure.step('Полльзователь успешно создан'):
        assert create_person.status_code == 200


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод manual_entry/create_new_card')
def test_manual_entry_0005(create_new_card):
    with allure.step('Карта успешно создана'):
        assert create_new_card.status_code == 200


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод manual_entry/change_card_balance')
def test_manual_entry_0006(change_card_balance):
    with allure.step('Баланс карты успешно пополнен'):
        assert change_card_balance.status_code == 200


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод cardholders/search')
@pytest.mark.xfail(reason="Превышение привилегий | ISNG-1162")
def test_manual_entry_0007(change_all_role, search_card):
    with allure.step('Поиск карты не выполнился, так как нет роли CARD_INFO_READ или CARD_INFO_FULL'):
        assert search_card.status_code == 403


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод /limit/')
@pytest.mark.xfail(reason="Превышение привилегий | ISNG-1162")
def test_manual_entry_0008(change_all_role, limit_card, create_person):
    data = auth.StdClass()
    data.value = 223344
    data.limit_type = 'card'
    data.operation_type = 'payment'
    data.url = 'limit/daily'
    resp = limit_card(data)
    with allure.step('Лимиты не установились, так как нет роли CARD_INFO_FULL'):
        assert resp.status_code == 403


@allure.feature(FEATURE)
@allure.story('Проверка ролевой модели')
@allure.title('Метод admin/role/add/roleTemplateId/28')
def test_manual_entry_0009(change_all_role, change_admin_role):
    with allure.step('Роль не изменилсь, так как нет прав на изменение ролей'):
        assert change_admin_role.status_code == 403


@allure.feature(FEATURE)
@allure.story('Функциональная проверка методов для карт /limit/')
@allure.title('Проверка кода ответа')
@pytest.mark.parametrize('method', ['daily', 'monthly', 'yearly'])
@pytest.mark.parametrize('limit_type, operation_type, value, in_base', [
    ('card', 'payment', 223344, 'climit'),
    ('card', 'all', 223344, 'alimit'),
    ('card', 'retail', 223344, 'rlimit'),
])
def test_manual_entry_0010(limit_card, create_person, method, limit_type, operation_type, value, in_base):
    """/hap/limit/daily | payment"""
    data = auth.StdClass()
    data.value = value
    data.limit_type = limit_type
    data.operation_type = operation_type
    data.url = 'limit/' + method
    resp = limit_card(data)
    with allure.step('Код ответа 200 метода limit/{} тип операции {}-{}'.format(method, limit_type, operation_type)):
        assert resp.status_code == 200
    resp = json.loads(create_person.text)
    app_id = resp['appId']
    if method == 'yearly':
        method = method[:-2]
    with allure.step('Сравнение установленного значения лимита {} со значением в БД'.format(value)):
        assert data.value == get_card_limit(app_id)[method + in_base]
    # обнуляю лимиты
    data.value = -1
    with allure.step('Обнуляем установленный лимит'):
        limit_card(data)


def convert_card(card):
    snew = "".join((card[:6], "XXXXXX", card[12:]))
    card = ' '.join([snew[i:i + 4] for i in range(0, len(snew), 4)])
    return card


def format_auth_data(data):
    ARN = get_arn(data['fseqno'])
    if ARN:
        arn = ARN[0]
    else:
        arn = ' -'
    arr = list()
    arr.append(data['description'] + data['cmscode'])
    arr.append(data['keydate'].strftime("%Y-%m-%d"))
    if data['datemercbatch'] is not None:
        arr.append(data['datemercbatch'].strftime("%Y-%m-%d"))
    else:
        arr.append('')
    arr.append(f'{data["rnn"]}/{arn}')
    if data['rnn'] is not None:
        arr.append(dbquery.Dbquery.get_auth_code([data["rnn"]]))
    if data['posdata'] is not None:
        arr.append(data['posdata'])
    else:
        arr.append('')
    arr.append(convert_card(data['card']))
    arr.append(data['appid'])
    if data['accotbval'] is not None:
        arr.append("{:.2f}".format(data['accotbval']))
    else:
        arr.append('')
    arr.append("{:.2f}".format(data['transvalue']))
    arr.append(data['transcur'])
    arr.append("{:.2f}".format(data['billvalue']))
    arr.append(data['billcur'])
    if data['origbillvalue'] is not None:
        arr.append("{:.2f}".format(data['origbillvalue']))
    else:
        arr.append('')
    if data['origbillcur'] is not None:
        arr.append(data['origbillcur'])
    else:
        arr.append('')
    if data['mercname'] is not None:
        arr.append(data['mercname'])
    else:
        arr.append(data['de43'])
    arr.append(data['mcc'])
    return arr


def format_row(row):
    if row[8] is not None:
        row[8] = "{:.2f}".format(float(row[8]))
    row[9] = "{:.2f}".format(float(row[9]))
    row[11] = "{:.2f}".format(float(row[11]))
    if row[13]:
        row[13] = "{:.2f}".format(float(row[13]))
    return row


@allure.feature(FEATURE)
@allure.story('Функциональная проверка методов генерации репортов /reports/transactions/card')
@allure.title('Проверка значений')
@pytest.mark.parametrize('rrn, arn', [(rrn, arn), (rrn1, arn1)])
def test_manual_entry_0011(generate_statement_report, rrn, arn):
    card_code = dbquery.Dbquery.get_cardcode_by_pan([card17['de002']])
    with allure.step('Получам id по карте для генерации запроса'):
        code_id = convert_card_code(card_code)
    params = {
        'id': code_id,
        'fromDate': from_date,
        'toDate': to_date
    }
    with allure.step('Отправляем запрос для генерации отчета'):
        response = generate_statement_report(params)
    filename = test_dir + '/../../../temp/transactions_' + code_id + '_' + from_date + '_' + to_date + '_' + str(
        datetime.timestamp(datetime.now())) + '.xlsx'
    with open(filename, 'wb') as f:
        f.write(response.content)
    search_cell = f'{rrn}/{arn}'
    with allure.step('Парсим отчет, находим строку с искомым параметром'):
        row_from_file = ParseXLSX(filename, 'Sheet1')
        row = row_from_file.search_value_in_row(search_cell)
    with allure.step('Получаем данные из БД для сравнения с данными из отчета'):
        expected_data = dbquery.Dbquery.get_auth_data([rrn])
    format_data = format_auth_data(expected_data)
    with allure.step('Сравниваем'):
        assert format_row(row) == format_data


@allure.feature(FEATURE)
@allure.story('Проверка методов manual_entry')
@allure.title('Метод manual_entry/change_card_balance')
def test_manual_entry_0012(change_card_balance):
    with allure.step('Баланс карты не поплнен, так как нет роли {}'.format(ROLE)):
        assert change_card_balance.status_code == 200
    print(type(change_card_balance.text))


def test_01():
    # cnp.send_data()
    # print(cnp.send_data().text)
    # auh1 = auth.VSDCAuth(card1['de002'], card1['de014'], 760, 978, card1['de035'], card1['de052'],
    #                   card1['de055'])
    # auh1 = auth.CPToken(card1['de002'], card1['de014'], 760, 978, card1['de035'], '4785673328152165')
    # cash = auth.Cash(card1['de002'], card1['de014'], 760, 978, card1['de035'], card1['de052'], card1['de055_2'])
    # oct = auth.OCT(card1['de002'], card1['de014'], 760, 643)

    # auh.send_data()
    # cash.send_data()
    cnp = auth.CNPAuth(card1['de002'], card1['de014'], 1000, 978)
    # cnp.de060 = '010000000702'
    resp = cnp.send_data()
    transastion = trans.Posting(cnp.__dict__)
    print(transastion.make_data_vi())
    # de062 = cnp.de062
    # r = json.loads(resp.text)
    # data = {key: value for (key, value) in r['data']['data'].items()}
    # print(data['de007'])
    # cnp.make_reversal(data['de007'], data['de011'], data['de037'], data['de038'], de062)


@pytest.fixture
def get_card(card_env, request):
    return card_env[request.param]


@pytest.mark.repeat(5)
@pytest.mark.parametrize("get_card", ["card2", "card3"], indirect=True)
@pytest.mark.parametrize("merchant_country_cod",
                         ["FUMINOR033-A. SAHAROVA 20RIGA         GB",])
def test_posting(get_card, merchant_country_cod):
    card = get_card
    OCT = auth.OCT(card['de002'], card['de014'], 2000, 978)
    OCT.de043 = merchant_country_cod
    CNPToken = auth.CNPToken(card['de002'], card['de014'], 600, 978)
    CNPToken.de043 = merchant_country_cod
    AFT = auth.AFT(card['de002'], card['de014'], 700, 978)
    AFT.de043 = merchant_country_cod
    Recurring = auth.Recurring(card['de002'], card['de014'], 100, 978)
    Recurring.de043 = merchant_country_cod
    Refund = auth.Refund(card['de002'], card['de014'], 1000, 978)
    Refund.de043 = merchant_country_cod
    data_mult = dict()
    data_mult[0] = OCT.send_data()
    data_mult[1] = CNPToken.send_data()
    data_mult[2] = AFT.send_data()
    data_mult[3] = Recurring.send_data()
    data_mult[4] = Refund.send_data()
    t1 = trans.Posting(data_mult)
    t1.make_posting()


@pytest.mark.repeat(4)
@pytest.mark.parametrize("merchant_country_cod",
                         ["FUMINOR033-A. SAHAROVA 20RIGA         GB", "FUMINOR033-A. SAHAROVA 20RIGA         TR"])
def test_posting_cash(card_env, merchant_country_cod):
    card = card_env
    MCash = auth.MCash(card['card1']['de002'], card['card1']['de014'], 600, 978, card['card1']['de035'],
                       card['card1']['de052'], card['card1']['de055'])
    MCash.de043 = merchant_country_cod

    ATMCash = auth.ATMCash(card['card1']['de002'], card['card1']['de014'], 700, 978, card['card1']['de035'],
                           card['card1']['de052'], card['card1']['de055'])
    ATMCash.de043 = merchant_country_cod
    VSDC = auth.VSDC(card['card1']['de002'], card['card1']['de014'], 800, 978, card['card1']['de035'],
                     card['card1']['de052'], card['card1']['de055'])
    VSDC.de043 = merchant_country_cod
    CPToken = auth.CPToken(card['card1']['de002'], card['card1']['de014'], 500, 978, card['card1']['de035'])
    CPToken.de043 = merchant_country_cod
    data_mult = dict()
    data_mult[0] = MCash.send_data()
    data_mult[1] = ATMCash.send_data()
    data_mult[2] = VSDC.send_data()
    data_mult[3] = CPToken.send_data()
    # t1 = trans.Posting(data_mult)
    # t1.make_posting()


def test_encode_ebcdic():
    print(auth.Auth.decode('E5F0F0F1F0F0F1F4F6F2F1F2F2F4F4F7F9F7F6F7F6F4F9F1F0F4F1F5F5'))
    # print(auth.Auth.decode('C289958195838540C4898789A3819340D3899489A3858440C28995819583'))
    # print(auth.Auth.decode('C8A48240F2F640C8A495A2A69699A38840D38195856B40C393858392888581A396956B'))
    # print(auth.Auth.decode('C393858392888581A39695'))
    # print(auth.Auth.decode('F8F2F6'))
    # print(auth.Auth.decode('F0F4'))
    # print(auth.Auth.decode('89829996408194819989938496'))


def test_trans(card_env):
    card = card_env
    CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 1000, 978)
    STIP = CNPToken.make_stip('00')
    CNPToken.send_data(STIP)
    # data_mult = dict()
    # data_mult[0] = CNPToken.send_data()
    # t1 = trans.Posting(data_mult)
    # t1.make_posting()


def calculate_trans(data):
    credit = 0
    debit = 0
    for val in data:
        # print(val)
        if (val['creditdebit'] == 0):
            debit = round(debit + val['billvalue'], 2)
        else:
            credit = round(credit + val['billvalue'], 2)

    # print(f"credit: {credit}; debit: {debit}")
    return {'credit': credit, 'debit': debit}


def get_exchange_rate(auth_val, bill_val):
    return round(auth_val / bill_val, 4)


def test_create_person():
    # add_role()
    card_data = card_api.PersonData('00010001', '100002', FIRST_NAME, LAST_NAME)
    card_data.create()
    # card_data.send_data()
    # resp = api_client.post(path='manual_entry/create_new_person',
    #                        headers=headers,
    #                        json=card_data.make_data(),
    #                        auth=auth.BearerAuth(get_token))
    # print(json.dumps(json.loads(resp.text), sort_keys=True, indent=4))
    # with allure.step('Создали нового персона'):
    #     return resp


@pytest.fixture
def get_card(card_env, request):
    return card_env[request.param]


@pytest.mark.parametrize("get_card", ["card2", "card3"], indirect=True)
def test_indirect(get_card):
    card = get_card
    assert len(get_card) == 3
