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


class CardBalance:

    def __init__(self, amount, card_id, trans_type):
        self.amount = amount
        self.card_id = card_id
        self.trans_type = trans_type

    def get_fi_code(self):
        fi_code = self.card_id.split('-')[0]
        return fi_code

    def make_data(self):
        data = {
            'amount': self.amount,
            'cardId': self.card_id,
            'ccyCode': '978',
            'fiCode': self.get_fi_code(),
            'mtype': 'status',
            'rid': '',
            'sign': '',
            'transType': self.trans_type
        }
        return json.dumps(data)


card = CardBalance('200', '00020001-625661427214', 'D')
print(card.make_data())


class PersonData:
    def __init__(self, agent_id, product_id, name, last_name):
        self.productId = product_id
        self.name = name
        self.last_name = last_name
        self.agent_id = agent_id

    def make_data(self):
        data = {
            "address": {
                "address": "street?build?flat_office",
                "city": "Kursk",
                "country": "643",
                "mailFirstName": self.name,
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
                    "mailFirstName": self.name,
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
                "firstName": self.name,
                "lastName": self.last_name,
                "middleName": "{{$randomAbbreviation}}",
                "nationality": "643",
                "passportId": "3809100100"
            },
            "sign": ""
        }
        return data


class CardData(PersonData):
    def __init__(self, account_id, person_id, agent_id, product_id, name, last_name):
        super().__init__(agent_id, product_id, name, last_name)
        self.account_id = account_id
        self.person_id = person_id




name = "maleksander" + str(random.randint(10, 99))
lastname = "maaazzz" + str(random.randint(10, 99))

l = PersonData('00020001', '900003', name, lastname)
print(l.make_data())
