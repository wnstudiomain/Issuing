import json
import random


class Auth:
    @staticmethod
    def encode(value):
        val = value.encode('cp037')
        return binascii.hexlify(val).decode('utf-8')


def encode_ebcdic(text):
    return text.decode('utf-8').encode('cp037')


def str_to_bcd(text):
    return bytes(str).decode('hex')


def str_to_binary(str):
    return int(str, 16)


def str_to_bcd(str):
    return bytes(str, encoding='utf8').decode('utf-8').encode('cp037')


import binascii


def bin2hex(str1):
    bytes_str = bytes(str1, 'utf-8')
    return binascii.hexlify(bytes_str)


a = "\xf4\xf7\xf8\xf5\xf6\xf7\xf3\xf3\xf2\xf8\xf1\xf5"
c = bin2hex(a)

print(c)
print(str_to_bcd('478567332815'))

print(Auth.encode('478567332815'))


class BearerAuth:
    def __init__(self, token):
        self.token = token

    def __call__(self, req):
        req.headers["Authorization"] = "Bearer " + self.token
        return req


class StdClass:
    pass


class PersonData:
    def __init__(self, agent_id, product_id, first_name, last_name):
        self.productId = product_id
        self.first_name = first_name
        self.last_name = last_name
        self.agent_id = agent_id

    def make_data(self):
        data = {
            "address": {
                "address": "street?build?flat_office",
                "city": "Kursk",
                "country": "643",
                "mailFirstName": self.first_name,
                "mailLastName": self.last_name,
                "zipCode": "305005"
            },
            "contact": {
                "email": "maaazzz@mail.ru",
                "phone": "+790452749999"
            },
            "identificator": {
                "agentIdentificator": self.agent_id,
                "rid": ""
            },
            "issuingData": {
                "accountId": "",
                "appId": "",
                "deliveryAddress": {
                    "address": "street?build?flat_office",
                    "city": "Kursk",
                    "country": "643",
                    "mailFirstName": self.first_name,
                    "mailLastName": self.last_name,
                    "state": "KurskState",
                    "zipCode": "305005"
                },
                "personId": "",
                "productId": self.productId,
                "urgencyIssuing": 1,
                "welcomePack": 1
            },
            "person": {
                "contactCode": "apitest",
                "dateOfBirthday": "1990-03-23",
                "firstName": self.first_name,
                "lastName": self.last_name,
                "middleName": "{{$randomAbbreviation}}",
                "nationality": "643",
                "passportId": "3809100100"
            },
            "sign": ""
        }
        return json.dumps(data)


class CardData(PersonData):
    def __init__(self, person_id, account_id, agent_id, product_id, first_name, last_name):
        super().__init__(agent_id, product_id, first_name, last_name)
        self.account_id = account_id
        self.person_id = person_id

    @staticmethod
    def get_agent_id(id):
        fi_code = id.split('-')[0]
        return fi_code

    def make_data(self):
        data = {
            "contact": {
                "email": "maaazzz@mail.ru",
                "phone": "+790452749999"
            },
            "identificator": {
                "agentIdentificator": self.get_agent_id(self.person_id),
                "rid": ""
            },
            "issuingData": {
                "accountId": self.account_id,
                "appId": "",
                "deliveryAddress": {
                    "address": "street?build?flat_office",
                    "city": "Kursk",
                    "country": "643",
                    "mailFirstName": "maleksander",
                    "mailLastName": "maaazzz",
                    "state": "KurskState",
                    "zipCode": "305005"
                },
                "personId": self.person_id,
                "productId": self.productId,
                "urgencyIssuing": 1,
                "welcomePack": 1
            },
            "sign": ""
        }
        return json.dumps(data)


class CardBalance(CardData):

    def __init__(self, amount, card_id, trans_type):
        self.amount = amount
        self.card_id = card_id
        self.trans_type = trans_type

    def make_data(self):
        data = {
            'amount': self.amount,
            'cardId': self.card_id,
            'ccyCode': '978',
            'fiCode': self.get_agent_id(self.card_id),
            'mtype': 'status',
            'rid': '',
            'sign': '',
            'transType': self.trans_type
        }
        return json.dumps(data)


class SearchCard:

    def __init__(self, app_id):
        self.app_id = app_id

    def make_data(self):
        data = {
            "appId": self.app_id,
            "currentPage": "",
            "firstName": "",
            "fullPan": "",
            "itemOnPage": "",
            "lastName": "",
            "otherNames": "",
            "panFirstSix": "",
            "panLastFour": "",
            "phone": ""
        }
        return json.dumps(data)


class CardLimitData:

    def __init__(self, limit_id, limit_type, operation_type, value):
        self.limit_id = limit_id
        self.limit_type = limit_type
        self.operation_type = operation_type
        self.value = value

    def make_data(self):
        data = {
            "id": self.limit_id,
            "limitType": self.limit_type,
            "operationType": self.operation_type,
            "value": self.value
        }
        return json.dumps(data)
