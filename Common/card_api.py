import pycountry
import random
from os import environ as env
from faker import Faker
from Common.client import APIClient
from hashlib import md5
import json
from Common.auth import BearerAuth

headers = {"Content-type": "application/json; charset=UTF-8"}


def get_token():
    ip = env.get('HAP_URL')
    api_client = APIClient(ip)
    login = env.get('HAP_LOGIN')
    password = env.get('HAP_PASSWORD').encode('utf-8')
    hash_pass = md5(password).hexdigest()
    resp = api_client.get(path='login',
                          params={'username': login, 'password': hash_pass})
    assert resp.status_code == 200
    data = json.loads(resp.text)
    token = data['token']
    print('get token')
    return token


class PersonData:
    fake = Faker()
    ctry = pycountry.countries.get(alpha_2=fake.country_code())

    def __init__(self, agent_id, product_id, first_name, last_name):
        self.productId = product_id
        self.first_name = first_name
        self.last_name = last_name
        self.agent_id = agent_id
        self.address = f"{self.fake.street_name()}?{self.fake.building_number()}?{random.randint(1, 99)}"
        self.city = self.fake.city()
        self.country = self.ctry.numeric
        self.zipcode = self.fake.postcode()
        self.phone = self.fake.country_calling_code().strip() + self.fake.msisdn()
        self.email = self.fake.ascii_free_email()

    def __call__(self):
        print("call")

    def make_data(self):
        data = {
            "address": {
                "address": self.address,
                "city": self.city,
                "country": self.country,
                "mailFirstName": self.first_name,
                "mailLastName": self.last_name,
                "zipCode": self.zipcode
            },
            "contact": {
                "email": self.email,
                "phone": self.phone[0:11]
            },
            "identificator": {
                "agentIdentificator": self.agent_id,
                "rid": ""
            },
            "issuingData": {
                "accountId": "",
                "appId": "",
                "deliveryAddress": {
                    "address": self.address,
                    "city": self.city,
                    "country": self.country,
                    "mailFirstName": self.first_name,
                    "mailLastName": self.last_name,
                    "zipCode": self.zipcode
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
                "middleName": "",
                "nationality": self.country,
                "passportId": "3809100100"
            },
            "sign": ""
        }
        return data

    def create(self):
        self.make_data()
        token = get_token()
        ip = env.get('HAP_URL')
        api_client = APIClient(ip)
        resp = api_client.post(path='manual_entry/create_new_person',
                               headers=headers,
                               json=self.make_data(),
                               auth=BearerAuth(token))
        print(json.dumps(json.loads(resp.text), sort_keys=True, indent=4))
        return resp


class CardData(PersonData):
    def __init__(self, person_id, account_id, agent_id, product_id, first_name, last_name):
        super().__init__(agent_id, product_id, first_name, last_name)
        self.account_id = account_id
        self.person_id = person_id

    @staticmethod
    def get_agent_id(ids):
        fi_code = ids.split('-')[0]
        return fi_code

    def make_data(self):
        data = {
            "contact": {
                "email": self.email,
                "phone": self.phone
            },
            "identificator": {
                "agentIdentificator": self.get_agent_id(self.person_id),
                "rid": ""
            },
            "issuingData": {
                "accountId": self.account_id,
                "appId": "",
                "deliveryAddress": {
                    "address": self.address,
                    "city": self.city,
                    "country": self.country,
                    "mailFirstName": self.first_name,
                    "mailLastName": self.last_name,
                    "zipCode": self.zipcode
                },
                "personId": self.person_id,
                "productId": self.productId,
                "urgencyIssuing": 1,
                "welcomePack": 1
            },
            "sign": ""
        }
        return data


class CardBalance:

    def __init__(self, amount, card_id, trans_type):
        self.amount = amount
        self.card_id = card_id
        self.trans_type = trans_type

    def make_data(self):
        data = {
            'amount': self.amount,
            'cardId': self.card_id,
            'ccyCode': '978',
            'fiCode': CardData.get_agent_id(self.card_id),
            'mtype': 'status',
            'rid': '',
            'sign': '',
            'transType': self.trans_type
        }
        return data
