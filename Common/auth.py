import datetime
from abc import abstractmethod
from Common.client import APIClient
import json
import random
from os import environ as env
from Common import ConstantNL4 as Card, dbquery
import pycountry
import time


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
        self.de011 = self._pref11field()
        self.de012 = '*'
        self.de013 = '*'
        self.de014 = de014
        self.de018 = '5812'
        self.de019 = '840'
        self.de022 = '0710'
        self.de025 = '00'
        self.de032 = '498750'
        self.de037 = self._pref37field() + self.de011
        self.de041 = 'TERMID01'
        self.de042 = '498750000236704'
        self.de043 = 'FUMINOR033-A. SAHAROVA 20RIGA         LV'
        self.de049 = de049
        self.de051 = '978'
        self.de056 = {
            '01': {
                '1': self.encode('V0010013821083272189654140003')
            }
        }
        self.de060 = '05000010'
        self.de062 = {
            '23': 'I ',
            '2': '3001633827' + str(random.randint(10000, 99999))
        }
        self.de063 = '8000000002'

    @staticmethod
    def _pref11field():
        times = str(time.time())
        new_time = times.split('.')[0][-4:] + times.split('.')[1][0:2]
        return new_time

    @staticmethod
    def _pref37field():
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
                    'de056': self.de056,
                    'de060': self.de060,
                    'de062': self.de062,
                    'de063': self.de063,
                }
        }
        for name, val in kwargs.items():
            data['data'][name] = val
        # print(json.dumps(data, sort_keys=True, indent=4))
        return data

    @staticmethod
    def make_token():
        return f'4785673328{random.randint(000000, 999999)}'

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
            data['data']['mti_resp'] = response_data['mti']
        print(json.dumps(response_data, sort_keys=True, indent=4))
        return data['data']

    def make_reversal(self, de038=None, de002=None, de007=None, de011=None, de032=None, de037=None, de042=None,
                      tid=None):
        mti = self.mti
        self.mti = '0400'
        self.de063 = 'A0000000022501'
        if de002 is not None:
            self.de002 = de002
        if de011 is not None:
            self.de011 = de011
        if de032 is not None:
            self.de032 = de032
        if de037 is not None:
            self.de037 = de037
        if de042 is not None:
            self.de042 = de042
        if tid is not None:
            self.de062['2'] = tid
        if de007 is not None:
            de007_original = de007
        else:
            de007_original = self.de007
        if de007 is not None and de011 is not None and de032 is not None:
            de090 = mti + de011 + de007 + de032.zfill(11) + '00000000000'
        else:
            de090 = mti + self.de011 + de007_original + self.de032.zfill(11) + '00000000000'
        self.de007 = self._pref07field()
        if de038 is not None:
            return self._make_data(de038=de038, de090=de090)
        else:
            return self._make_data(de090=de090)

    def make_partial_reversal(self, new_summ, de038=None, de002=None, de007=None, de011=None, de032=None, de037=None,
                              de042=None, tid=None):
        mti = self.mti
        self.mti = '0400'
        self.de063 = 'A0000000022504'
        if de002 is not None:
            self.de002 = de002
        if de007 is not None:
            self.de007 = de007
        if de011 is not None:
            self.de011 = de011
        if de032 is not None:
            self.de032 = de032
        if de037 is not None:
            self.de037 = de037
        if de042 is not None:
            self.de042 = de042
        if tid is not None:
            self.de062['2'] = tid
        if de007 is not None:
            de007_original = de007
        else:
            de007_original = self.de007
        if de007 is not None and de011 is not None and de032 is not None:
            de090 = mti + de011 + de007 + de032.zfill(11) + '00000000000'
        else:
            de090 = mti + self.de011 + de007_original + self.de032.zfill(11) + '00000000000'
        self.de007 = self._pref07field()
        de061 = str(new_summ).zfill(36)
        de095 = str(new_summ).zfill(12) + '000000000000000000000000000000'
        if de038 is not None:
            return self._make_data(de038=de038, de090=de090, de061=de061, de095=de095)
        else:
            return self._make_data(de090=de090, de061=de061, de095=de095)

    def make_stip(self, de039):
        self.mti = '0120'
        return self._make_data(de039=de039)


class CNPAuth(Auth):

    def __init__(self, de002, de014, de004, de049):
        super().__init__(de002, de014, de004, de049)
        self.de044 = '              2'
        # Field 22—Point-of-Service Entry Mode Code
        # Card-Not-Present Recurring Payment Transactions: The value in field positions 1
        # and 2 must be 01 or 10
        # Position 3: PIN Entry Capability
        # 2 - Terminal cannot accept PINs
        self.de022 = '0120'
        # Field 25—Point-of-Service Condition Code
        # 59 - E-commerce request through public network - Internet transaction.
        self.de025 = '59'
        self.de003 = '000000'
        # Field 60—Additional POS Information
        # 60.1 - 5 - On premises of cardholder, unattended eP
        # 60.2 - 1 - Terminal not used
        # 60.8 - 05 - SET with cardholder certificate
        self.de060 = '5100000005'
        # доработать в Сашином приложении
        # self.de126 = {
        #     '9': '0009010871161500000002589782437559441171',
        #     '13': self.encode('C'),
        #     '20': self.encode('9')
        # }

    def _get_data(self):
        return self._make_data(de044=self.de044)


class VSDC(Auth):

    def __init__(self, de002, de014, de004, de049, de035, de052, de055):
        super().__init__(de002, de014, de004, de049)
        self.de035 = de035
        self.de055 = de055
        self.de052 = de052
        self.de023 = '001'
        self.de053 = '2001010100000000'

    def _get_data(self):
        return self._make_data(de035=self.de035, de053=self.de053, de055=self.de055, de023=self.de023, de052=self.de052)


class CNPToken(CNPAuth):

    def __init__(self, de002, de014, de004, de049, token=Auth.make_token()):
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

    def __init__(self, de002, de014, de004, de049, de035, token=Auth.make_token()):
        super().__init__(de002, de014, de004, de049, token)
        self.de044 = '    2   2'
        self.de035 = de035
        self.de060 = '05000040'
        self.de022 = '0710'
        self.de025 = '00'

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


class ATMCash(VSDC):

    def __init__(self, de002, de014, de004, de049, de035, de052, de055):
        super().__init__(de002, de014, de004, de049, de035, de052, de055)
        self.de035 = de035
        self.de052 = de052
        self.de055 = de055
        self.de003 = '012000'
        self.de018 = '6011'
        self.de022 = '0510'
        self.de025 = '02'
        self.de060 = '25000010'

        def _get_data(self):
            return self._make_data(de053=self.de053)


class MCash(VSDC):

    def __init__(self, de002, de014, de004, de049, de035, de052, de055):
        super().__init__(de002, de014, de004, de049, de035, de052, de055)
        self.de035 = de035
        self.de052 = de052
        self.de055 = de055
        self.de003 = '012000'
        self.de018 = '6010'
        self.de022 = '0710'
        self.de025 = '00'
        self.de060 = '05000010'


class Recurring(CNPAuth):
    def __init__(self, de002, de014, de004, de049):
        super().__init__(de002, de014, de004, de049)
        self.de025 = '08'
        self.de022 = '1020'
        self.de060 = '0100000002'
        # self.de126 = '0008000000000000D9'


class OCT(Auth):

    def __init__(self, de002, de014, de004, de049):
        super().__init__(de002, de014, de004, de049)
        self.de003 = '260000'
        self.de018 = '4829'
        self.de025 = '05'
        self.de022 = '0100'
        # Field 48, Usage 37—Original Credit Transaction (OCT)
        self.de048 = 'OCT000000031071981'
        # Field 60—Additional POS Information
        self.de060 = '0100000007'
        self.de104 = '5700040102C6C45F007C0110F0F0F0F0F0F0F0F0F1F6F1F9F8F8F6F7031EC289958195838540C4898789A3819340D3899489A3858440C289958195830423C8A48240F2F640C8A495A2A69699A38840D38195856B40C393858392888581A396956B050BC393858392888581A396950703F8F2F60802F0F40A0D89829996408194819989938496 '

    def _get_data(self):
        return self._make_data(de048=self.de048, de104=self.de104)


class AFT(CNPAuth):

    def __init__(self, de002, de014, de004, de049):
        super().__init__(de002, de014, de004, de049)
        self.de003 = '100000'
        self.de018 = '4829'
        self.de104 = '5700040102D7D7'

    def _get_data(self):
        return self._make_data(de104=self.de104, de044=self.de044)


class Refund(CNPToken):

    def __init__(self, de002, de014, de004, de049, token=Auth.make_token()):
        super().__init__(de002, de014, de004, de049, token)
        self.de003 = '200000'


# Инитная операция в отеле
class HotelAuth(CPToken):

    def __init__(self, de002, de014, de004, de049, de035, token=Auth.make_token()):
        super().__init__(de002, de014, de004, de049, de035, token)
        # MCC 3618: Отели, мотели, курорты
        self.de018 = '3618'
        self.de060 = '050000400002'
        self.de043 = 'THE BALMORAL HOTEL       EDINBURGH    GB'

    def make_inc(self, de004, de049):
        self.de063 = 'A0000000023900'
        self.de007 = self._pref07field()
        self.de004 = de004
        self.de006 = de004
        self.de049 = de049
        self.de051 = de049
        return self._make_data()


class AFD(CPToken):

    def __init__(self, de002, de014, de004, de049, de035):
        super().__init__(de002, de014, de004, de049, de035)
        self.de018 = '5542'
        self.de041 = '60050063'
        self.de043 = 'WM MORRISONS PETROL OP   BOLTON       GB'
        self.de060 = '350000400001'

    def afd_advice(self, de038, de004, de006=None):
        self.mti = '0120'
        self.de004 = de004
        if de006 is None:
            self.de006 = de004
        else:
            self.de006 = de006
        self.de007 = self._pref07field()
        self.de011 = self._pref11field()
        return self._make_data(de038=de038)


def convert_tlv():
    str = '0100729F34034402029F2701809F3501259F090200969F3303E0B8E89505008000E0009F3704B9735CBE9F100706001203A420029F26080B8D2E1C638BBED29F36020006820238009C01009F1A0208269A032109159F02060000000001005F2A0208269F03060000000000008407A0000000031010'
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


convert_tlv()
