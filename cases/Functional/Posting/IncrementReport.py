import time
import unittest

import pytest

from Common import dbquery
import Common.auth as auth
from Common import trans
from os import environ as env
from Common.client import APIClient
import json, xmltodict

header_soap = {'content-type': 'text/xml'}
ip = env.get('WS_POSTING_URL')
body_report = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
xmlns:web="http://webservice.ecp.com/"> <soapenv:Header/> <soapenv:Body> <web:getIncremenalAuths/> </soapenv:Body> 
</soapenv:Envelope> """


class IncrementalReport(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def injector_fixture(self, card_env):
        self.card_env = card_env

    @staticmethod
    def get_incremenal_auths_post():
        api_client = APIClient(ip)
        response = api_client.post(path='WebService-Posting/Posting',
                                   headers=header_soap,
                                   body=body_report)
        # response_data = json.loads(response.text)
        json_response = xmltodict.parse(response.text)
        auth_record = json.dumps(
            json_response['S:Envelope']['S:Body']['ns2:getIncremenalAuthsResponse']['return']['authRecord'],)
        return json.loads(auth_record)

    def test_posting_init(self):
        # Делаю запрос перед тестом, что бы узнать количество текущий записей
        auth_record_before = len(self.get_incremenal_auths_post())
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        assert init['de039'] == '00'
        first_inc = Hotel.make_inc(3000, 978)
        first_inc_resp = Hotel.send_data(first_inc)
        assert first_inc_resp['de039'] == '00'
        second_inc = Hotel.make_inc(2000, 978)
        second_inc_resp = Hotel.send_data(second_inc)
        assert second_inc_resp['de039'] == '00'
        third_inc = Hotel.make_inc(1000, 978)
        third_inc_resp = Hotel.send_data(third_inc)
        assert third_inc_resp['de039'] == '00'
        data_mult = dict()
        data_mult[0] = init
        t1 = trans.Posting(data_mult)
        t1.make_posting()
        aq_trans_data = trans.get_data_trans_from_aq(init['de037'])
        self.assertEqual(t1.arn, aq_trans_data['acquirer_reference_number'])
        auth_record_after = self.get_incremenal_auths_post()
        auth_record_after_count = len(auth_record_after)
        # Проверяю что появилась еще одна новая запись
        assert auth_record_after_count == auth_record_before + 1
        actual_dict = {}
        for auth_list in auth_record_after:
            if auth_list['rrn'] == init['de037']:
                actual_dict = auth_list
        accno = dbquery.Dbquery.get_accno_by_pan((init['de002'],))
        count = '3'
        self.assertDictEqual(actual_dict, {'accno': accno[0], 'count': count, 'rrn': init['de037']})

    def test_posting_init_1(self):
        # Делаю запрос перед тестом, что бы узнать количество текущий записей
        auth_record_before = len(self.get_incremenal_auths_post())
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        assert init['de039'] == '00'
        first_inc = Hotel.make_inc(3000, 978)
        first_inc_resp = Hotel.send_data(first_inc)
        assert first_inc_resp['de039'] == '00'
        second_inc = Hotel.make_inc(2000, 978)
        second_inc_resp = Hotel.send_data(second_inc)
        assert second_inc_resp['de039'] == '00'
        data_mult = dict()
        init['de004'] = '000000005120'
        init['de006'] = '000000005120'
        data_mult[0] = init
        t1 = trans.Posting(data_mult)
        t1.make_posting()
        aq_trans_data = trans.get_data_trans_from_aq(init['de037'])
        self.assertEqual(t1.arn, aq_trans_data['acquirer_reference_number'])
        auth_record_after = self.get_incremenal_auths_post()
        auth_record_after_count = len(auth_record_after)
        # Проверяю что появилась еще одна новая запись
        assert auth_record_after_count == auth_record_before + 1
        actual_dict = {}
        for auth_list in auth_record_after:
            if auth_list['rrn'] == init['de037']:
                actual_dict = auth_list
        accno = dbquery.Dbquery.get_accno_by_pan((init['de002'],))
        count = '2'
        self.assertDictEqual(actual_dict, {'accno': accno[0], 'count': count, 'rrn': init['de037']})

    def test_posting_init_2(self):
        # Делаю запрос перед тестом, что бы узнать количество текущий записей
        auth_record_before = len(self.get_incremenal_auths_post())
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        data_mult = dict()
        data_mult[0] = init
        t1 = trans.Posting(data_mult)
        t1.make_posting()
        aq_trans_data = trans.get_data_trans_from_aq(Hotel.de037)
        self.assertEqual(t1.arn, aq_trans_data['acquirer_reference_number'])
        auth_record_after = self.get_incremenal_auths_post()
        auth_record_after_count = len(auth_record_after)
        # Проверяю что не появилась еще одна новая запись
        self.assertEqual(auth_record_after_count, auth_record_before)


