import datetime
from abc import abstractmethod
from faker import Faker
from Common.client import APIClient
import json
import random
from os import environ as env
from Common import ConstantNL4 as Card, dbquery
import pycountry

card17 = Card.ConstantNL4.CARD_6807_NL4


def encode_ebcdic(text):
    return text.decode('utf-8').encode('cp037')


def decode_ebcdic(text):
    return text.decode('cp037').encode('utf-8')


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


class BearerAuth:
    def __init__(self, token):
        self.token = token

    def __call__(self, req):
        req.headers["Authorization"] = "Bearer " + self.token
        return req


class StdClass:
    pass


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
        return data


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
        return data


class Auth:
    headers = {"Content-type": "application/json; charset=UTF-8"}

    def __init__(self, de002, de014, de004, de049):
        self.mti = '0100'
        self.de002 = de002
        self.de003 = '000000'
        self.de004 = str(de004)
        self.de006 = str(de004)
        self.de007 = self._pref07field()
        self.de011 = dbquery.Dbquery.get_max_de011()
        self.de012 = '*'
        self.de013 = '*'
        self.de014 = de014
        self.de018 = '5812'
        self.de019 = '840'
        self.de022 = '0710'
        self.de025 = '00'
        self.de032 = '498750'
        self.de037 = self.pref37field() + self.de011
        self.de041 = 'TERMID01'
        self.de042 = '498750000236704'
        self.de043 = 'FUMINOR033-A. SAHAROVA 20RIGA         LV'
        self.de049 = de049
        self.de051 = de049
        self.de056 = {
            '01': {
                '1': self.encode('V0010013821083272189654140003')
            }
        }
        self.de060 = '05000010'
        self.de062 = {
            '1': 'E',
            '23': 'I ',
            '2': '3001633827' + str(random.randint(10000, 99999))
        }
        self.de063 = '8000000002'
        self.de039 = ''
        self.de038 = ''

    @staticmethod
    def pref37field():
        y = str(datetime.datetime.today().year)
        day = datetime.datetime.today().strftime("%j")
        h = datetime.datetime.today().strftime("%H")
        return y[3:4] + day + h

    @staticmethod
    def _pref07field():
        return datetime.datetime.today().strftime('%m%d%H%M%S')

    @staticmethod
    def encode(value):
        val = value.encode('cp037')
        return binascii.hexlify(val).decode('utf-8')

    @staticmethod
    def decode(value):
        return binascii.unhexlify(value).decode('cp037')

    def _make_data(self, **kwargs):
        data = {
            'data':
                {
                    'mti': self.mti,
                    'de002': self.de002,
                    'de003': self.de003,
                    'de004': str(self.de004).zfill(12),
                    'de006': str(self.de006).zfill(12),
                    'de007': self.de007,
                    'de011': self.de011,
                    'de012': self.de012,
                    'de013': self.de013,
                    'de014': self.de014,
                    'de018': self.de018,
                    'de019': self.de019,
                    'de022': self.de022,
                    'de025': self.de025,
                    'de032': self.de032,
                    'de037': self.de037,
                    'de041': self.de041,
                    'de042': self.de042,
                    'de043': self.de043,
                    'de049': str(self.de049),
                    'de051': str(self.de051),
                    # 'de056': self.de056,
                    'de060': self.de060,
                    'de062': self.de062,
                    'de063': self.de063,
                }
        }
        for name, val in kwargs.items():
            data['data'][name] = val
        # print(json.dumps(data, sort_keys=True, indent=4))
        return data

    @abstractmethod
    def _get_data(self):
        pass

    def send_data(self, data=None):
        data = data if data is not None else self._get_data()
        ip = env.get('SIM_URL')
        api_client = APIClient(ip)
        response = api_client.post(path='Simulator/sendJSON?mess=wrewrwr',
                                   headers=self.headers,
                                   json=data)
        response_data = json.loads(response.text)['data']['data']
        if response_data.get('de038') is not None:
            data['data']['de038'] = response_data['de038']
        if response_data.get('de039') is not None:
            data['data']['de039'] = response_data['de039']
        print(json.dumps(response_data, sort_keys=True, indent=4))
        return data['data']

    def make_reversal(self, de007, de011, de037, de038, de062):
        self.mti = '0400'
        self.de063 = 'A0000000022501'
        self.de011 = de011
        self.de037 = de037
        self.de062 = de062
        de090 = '0100' + self.de011 + de007 + self.de032.zfill(11) + '00000000000'
        data = self._make_data(de038=de038, de090=de090)
        self.send_data(data)


class CNPAuth(Auth):

    def __init__(self, de002, de014, de004, de049):
        super().__init__(de002, de014, de004, de049)
        self.de044 = '              2'
        self.de022 = '0100'
        self.de025 = '59'
        self.de003 = '000000'
        self.de060 = '0100000005'

    def _get_data(self):
        return self._make_data()


class VSDC(Auth):

    def __init__(self, de002, de014, de004, de049, de035, de052, de055):
        super().__init__(de002, de014, de004, de049)
        self.de035 = de035
        self.de055 = de055
        self.de052 = de052
        self.de023 = '001'

    def _get_data(self):
        return self._make_data(de035=self.de035, de055=self.de055, de023=self.de023, de052=self.de052)


class CNPToken(CNPAuth):

    def __init__(self, de002, de014, de004, de049, token):
        super().__init__(de002, de014, de004, de049)
        self.token = self.encode(token)
        self._2 = self.encode('  ')
        self._1f33 = self.encode('5382')
        self._3 = self.encode('40010075001')
        self._1f32 = self.encode('1')
        self._1f31 = self.encode('22')
        self._6 = self.encode('2406')
        self._7 = self.encode('03')
        self.de060 = '0900004007'

    def _make_123_68(self):
        data = {
            '68': {
                '1': self.token,
                '2': self._2,
                '1f33': self._1f33,
                '3': self._3,
                '1f32': self._1f32,
                '1f31': self._1f31,
                '6': self._6,
                '7': self._7
            }
        }
        return data

    def _get_data(self):
        return self._make_data(de123=self._make_123_68(), de044=self.de044)


class CPToken(CNPToken):

    def __init__(self, de002, de014, de004, de049, de035, token):
        super().__init__(de002, de014, de004, de049, token)
        self.de044 = '    2   2'
        self.de035 = de035
        self.de060 = '05000040'

    def _make_123_67_68(self):
        data = {
            **self._make_123_68(),
            '67': {
                '5': '04000000'
            },
        }
        return data

    def _get_data(self):
        return self._make_data(de035=self.de035, de044=self.de044, de123=self._make_123_67_68())


class Cash(Auth):

    def __init__(self, de002, de014, de004, de049, de035, de052, de055):
        super().__init__(de002, de014, de004, de049)
        self.de035 = de035
        self.de052 = de052
        self.de055 = de055
        self.de003 = '012000'
        self.de018 = '6011'
        self.de022 = '0510'
        self.de025 = '02'
        self.de053 = '2001010100000000'
        self.de060 = '25000010'

    def _get_data(self):
        return self._make_data(de035=self.de035, de052=self.de052, de055=self.de055)


class OCT(Auth):

    def __init__(self, de002, de014, de004, de049):
        super().__init__(de002, de014, de004, de049)
        self.de003 = '260000'
        self.de018 = '4829'
        self.de025 = '05'
        self.de022 = '0100'
        self.de048 = 'OCT000000031071981'
        self.de060 = '0100000007'

    def _get_data(self):
        return self._make_data()


def convert_de126():
    str = '660016C004F1F0F5F0D00EF1F0F5F0404040404040404040406800480110F4F6F3F6F6F3F1F9F4F1F0F0F1F4F5F102024040030BF4F0F0F1F0F0F3F0F2F7F30604F2F3F1F20702F0F28001008108F9F6F2F3F6F1F3F58201008301608401028503000D2F'
    i = 0
    data = dict()
    while i < len(str):
        tag = str[i:i + 2]
        length = int(str[i + 2:i + 6], 16)
        length_val = length * 2
        value = str[i + 6:i + length_val + 6]
        j = 0
        data[tag] = dict()
        leng = len(value)
        while j < len(value):
            dataset_tag = value[j:j + 2]
            dataset_length = int(value[j + 2:j + 4], 16)
            dataset_length_val = dataset_length * 2
            dataset_value = value[j + 4:j + dataset_length_val + 4]
            data[tag][dataset_tag] = dataset_value
            j = j + 4 + dataset_length_val
        # data[tag] = value
        i = i + 6 + length_val
    print(json.dumps(data, sort_keys=True, indent=4))


# convert_de126()
