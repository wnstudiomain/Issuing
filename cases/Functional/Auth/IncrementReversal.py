import time
import unittest
import pytest
from Common import dbquery
import Common.auth as auth
from Common import trans


class IncrementalAuth(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def injector_fixture(self, card_env):
        self.card_env = card_env

    # реверсал сматчился
    def test_reversal_positive(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        reversal = CNPToken.send_data(
            CNPToken.make_reversal())
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 10 == in_base[0]['detail']

    # полный реверсал на деклайн
    def test_reversal_decline(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        CNPToken.de014 = '2210'
        response = CNPToken.send_data()
        assert '05' == response['de039']
        reversal = CNPToken.send_data(
            CNPToken.make_reversal())
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 11 == in_base[0]['detail']

    # реверсал сума в de004 и de006 отличаются от ориг авторизации
    def test_reversal_positive2(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        reversal = CNPToken.make_reversal(response['de038'])
        reversal['data']['de004'] = '000000000700'
        reversal['data']['de006'] = '000000000700'
        CNPToken.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 10 == in_base[0]['detail']

    # две авторизации и реверсла на первую авторизацию
    def test_reversal_positive1(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response_1 = CNPToken.send_data()
        assert '00' == response_1['de039']
        CNPToken1 = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 700, 978)
        response_2 = CNPToken1.send_data()
        assert '00' == response_2['de039']
        reversal = CNPToken.send_data(
            CNPToken.make_reversal(response_1['de038']))
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 10 == in_base[0]['detail']

    # @pytest.mark.repeat(1)
    # Проверяю логику матчинга реверсала
    # Field 2
    # Field 11
    # Field 32
    # Field 37
    # Field 42
    # Field 62.2
    # и
    # Field 90
    # или
    # Field 38

    def test_reversal_bad_de011(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        CNPToken.de011 = '766977'
        reversal = CNPToken.send_data(
            CNPToken.make_reversal())
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 21 == in_base[0]['detail']

    def test_reversal_bad_de032(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        CNPToken.de032 = '498751'
        reversal = CNPToken.send_data(
            CNPToken.make_reversal())
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 21 == in_base[0]['detail']

    def test_reversal_bad_de037(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        CNPToken.de037 = '125217766977'
        reversal = CNPToken.send_data(
            CNPToken.make_reversal())
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 21 == in_base[0]['detail']

    def test_reversal_bad_de042(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        CNPToken.de042 = '498750000236701'
        reversal = CNPToken.send_data(
            CNPToken.make_reversal())
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 21 == in_base[0]['detail']

    def test_reversal_bad_tid(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        CNPToken.de062['2'] = '300163382721984'
        reversal = CNPToken.send_data(
            CNPToken.make_reversal())
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert 0 == in_base[0]['accepted']
        assert 21 == in_base[0]['detail']

    # матчим по 38 полю
    def test_reversal_bad_de090(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        reversal = CNPToken.make_reversal(de038=response['de038'])
        reversal['data']['de090'] = '000000000000000000000000000000000000000000'
        CNPToken.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 10

    # Убираю 11 поле из 90 поля
    def test_reversal_bad_de090_de011(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        reversal = CNPToken.make_reversal()
        reversal['data']['de090'] = response['mti'] + '675732' + response['de007'] + response['de032'].zfill(
            11) + '00000000000'
        reversal['data'].pop('de038', None)
        CNPToken.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 21

    def test_reversal_bad_de090_de007(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        reversal = CNPToken.make_reversal()
        reversal['data']['de090'] = response['mti'] + response['de011'] + '0910123917' + response['de032'].zfill(
            11) + '00000000000'
        reversal['data'].pop('de038', None)
        CNPToken.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 21

    # 32 поле не учитываем при формировании 90 поля
    def test_reversal_bad_de090_de032(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        reversal = CNPToken.make_reversal()
        reversal['data']['de090'] = response['mti'] + response['de011'] + response[
            'de007'] + '00000498751' + '00000000000'
        reversal['data'].pop('de038', None)
        CNPToken.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 10

    # Пробуем матчить без 38 и 90 поля
    def test_reversal_bad_de090_and_de038(self):
        card = self.card_env
        CNPToken = auth.CNPToken(card['card4']['de002'], card['card4']['de014'], 600, 978)
        response = CNPToken.send_data()
        assert '00' == response['de039']
        reversal = CNPToken.make_reversal()
        reversal['data'].pop('de090', None)
        reversal['data'].pop('de038', None)
        CNPToken.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((CNPToken.de037,))
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 21

    # Полный реверсал на инитную операцию
    def test_full_reversal_init(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        reversal = Hotel.make_reversal(de007=init['de007'], de011=init['de011'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        for t6_auth in in_base:
            assert t6_auth['accepted'] == 0
            assert t6_auth['detail'] == 10

    # Полный реверсал на последнюю инкрементную операцию
    def test_full_reversal_increment_last(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        reversal = Hotel.make_reversal(de007=second_inc['data']['de007'], de011=second_inc['data']['de011'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 10
        assert in_base[1]['accepted'] == 1
        assert in_base[1]['detail'] == 0
        assert in_base[-1]['accepted'] == 1
        assert in_base[-1]['detail'] == 0

    # Полный реверсал на первую инкрементную операцию
    def test_full_reversal_increment_first(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        reversal = Hotel.make_reversal(de011=first_inc['data']['de011'], de007=first_inc['data']['de007'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        assert in_base[1]['accepted'] == 0
        assert in_base[1]['detail'] == 10
        assert in_base[0]['accepted'] == 1
        assert in_base[0]['detail'] == 0
        assert in_base[-1]['accepted'] == 1
        assert in_base[-1]['detail'] == 0

    # Частичный реверсал на инитную операцию на меньшую сумму
    def test_partial_reversal_init(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        new_sum = 4500
        reversal = Hotel.make_partial_reversal(new_sum, de038=init['de038'])
        reversal['data']['de090'] = '000000000000000000000000000000000000000000'
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.1f}".format(new_sum * 0.01))
        assert in_base[-1]['accepted'] == 1
        assert in_base[-1]['detail'] == 10
        assert in_base[-1]['authvalue'] == expected_summ
        for t6_auth in in_base[:-1]:
            assert t6_auth['accepted'] == 0
            assert t6_auth['detail'] == 10

    # Частичный реверсал на инитную операцию на большую сумму
    def test_partial_reversal_init_summ(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        new_sum = 5500
        reversal = Hotel.make_partial_reversal(new_sum, de038=init['de038'], de007=init['de007'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.1f}".format(new_sum * 0.01))
        for t6_auth in in_base[1:]:
            assert t6_auth['accepted'] == 1
            assert t6_auth['detail'] == 0
        assert in_base[0]['authvalue'] == expected_summ
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 21

    # Частичный реверсал на инкрементную операцию, сумма меньше чем сумма в инкрементной операции
    def test_partial_increment_sum_less(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        new_sum = 1
        reversal = Hotel.make_partial_reversal(new_sum, de011=second_inc['data']['de011'],
                                               de007=second_inc['data']['de007'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.2f}".format(new_sum * 0.01))
        for t6_auth in in_base[1:]:
            assert t6_auth['accepted'] == 1
            assert t6_auth['detail'] == 0
        assert in_base[0]['authvalue'] == expected_summ
        assert in_base[0]['accepted'] == 1
        assert in_base[0]['detail'] == 10

    # Частичный реверсал на две инкрементных операции, сумма меньше чем сумма в инкрементной операции
    def test_partial_increment_sum_less_2(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        new_sum = 1
        reversal = Hotel.make_partial_reversal(new_sum, de038=second_inc['data']['de038'])
        Hotel.send_data(reversal)
        reversal1 = Hotel.make_partial_reversal(new_sum, de007=first_inc['data']['de007'],
                                                de011=first_inc['data']['de011'])
        Hotel.send_data(reversal1)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.2f}".format(new_sum * 0.01))
        assert in_base[0]['authvalue'] == expected_summ
        assert in_base[0]['accepted'] == 1
        assert in_base[0]['detail'] == 10
        assert in_base[1]['authvalue'] == expected_summ
        assert in_base[1]['accepted'] == 1
        assert in_base[1]['detail'] == 10
        assert in_base[2]['accepted'] == 1
        assert in_base[2]['detail'] == 0

    # Частичный реверсал на инкрементную операцию, сумма больше чем сумма в инкрементной операции
    def test_partial_increment_sum_more(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        new_sum = 2001
        reversal = Hotel.make_partial_reversal(new_sum, de038=second_inc['data']['de038'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.2f}".format(new_sum * 0.01))
        for t6_auth in in_base[1:]:
            assert t6_auth['accepted'] == 1
            assert t6_auth['detail'] == 0
        assert in_base[0]['authvalue'] == expected_summ
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 21

    # Полный реверсал на первую операцию с тегом 63.3
    def test_full_reversal_init_1(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        Hotel.de063 = 'A0000000023900'
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        reversal = Hotel.make_reversal(init['de038'], de007=init['de007'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        for t6_auth in in_base[:-1]:
            assert t6_auth['accepted'] == 1
            assert t6_auth['detail'] == 0
        assert in_base[-1]['accepted'] == 0
        assert in_base[-1]['detail'] == 10

    # Полный реверсал на инитную 120
    def test_full_reversal_init_120(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 100, 978, card['card4']['de035'])
        STIP = Hotel.make_stip('00')
        init = Hotel.send_data(STIP)
        Hotel.mti = '0100'
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        reversal = Hotel.make_reversal(de007=init['de007'], de011=init['de011'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        for t6_auth in in_base:
            assert t6_auth['accepted'] == 0
            assert t6_auth['detail'] == 10

    # все инкременты 120 и полный реверсал на последний инкремент
    def test_full_reversal_increment_120(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        first_inc['data']['de039'] = '00'
        first_inc['data']['mti'] = '0120'
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        second_inc['data']['de039'] = '00'
        second_inc['data']['mti'] = '0120'
        Hotel.send_data(second_inc)
        reversal = Hotel.make_reversal(de007=second_inc['data']['de007'], de011=second_inc['data']['de011'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 10
        assert in_base[1]['accepted'] == 1
        assert in_base[1]['detail'] == 0
        assert in_base[-1]['accepted'] == 1
        assert in_base[-1]['detail'] == 0

    # Частичный реверсал на инитную операцию на большую сумму
    def test_partial_reversal_init_summ_120(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        STIP = Hotel.make_stip('00')
        init = Hotel.send_data(STIP)
        Hotel.mti = '0100'
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        new_sum = 5500
        reversal = Hotel.make_partial_reversal(new_sum, de007=init['de007'], de011=init['de011'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.1f}".format(new_sum * 0.01))
        for t6_auth in in_base[1:]:
            assert t6_auth['accepted'] == 1
            assert t6_auth['detail'] == 0
        assert in_base[0]['authvalue'] == expected_summ
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 21

    # Частичный реверсал на инитную операцию на меньшую сумму
    def test_partial_reversal_init_summ_120_less(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        STIP = Hotel.make_stip('00')
        init = Hotel.send_data(STIP)
        Hotel.mti = '0100'
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        Hotel.send_data(second_inc)
        new_sum = 4500
        reversal = Hotel.make_partial_reversal(new_sum, de007=init['de007'], de011=init['de011'])
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.1f}".format(new_sum * 0.01))
        for t6_auth in in_base[:-1]:
            assert t6_auth['accepted'] == 0
            assert t6_auth['detail'] == 10
        assert in_base[-1]['authvalue'] == expected_summ
        assert in_base[-1]['accepted'] == 1
        assert in_base[-1]['detail'] == 10

    # Частичный реверсал на инитную операцию, затем два инкремента и полный реверсал на инитную
    def test_partial_reversal_init_3(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        STIP = Hotel.make_stip('00')
        init = Hotel.send_data(STIP)
        assert init['de039'] == '00'
        Hotel.mti = '0100'
        first_inc = Hotel.make_inc(3000, 978)
        first_inc_resp = Hotel.send_data(first_inc)
        assert first_inc_resp['de039'] == '00'
        second_inc = Hotel.make_inc(2000, 978)
        second_inc_resp = Hotel.send_data(second_inc)
        assert second_inc_resp['de039'] == '00'
        new_sum = 4500
        reversal = Hotel.make_partial_reversal(new_sum, de007=init['de007'], de011=init['de011'])
        reversal_resp = Hotel.send_data(reversal)
        assert reversal_resp['de039'] == '00'
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.1f}".format(new_sum * 0.01))
        for t6_auth in in_base[:-1]:
            assert t6_auth['accepted'] == 0
            assert t6_auth['detail'] == 10
        assert in_base[-1]['authvalue'] == expected_summ
        assert in_base[-1]['accepted'] == 1
        assert in_base[-1]['detail'] == 10
        Hotel.mti = '0100'
        third_inc = Hotel.make_inc(3500, 978)
        third_inc_resp = Hotel.send_data(third_inc)
        assert third_inc_resp['de039'] == '00'
        fourth_inc = Hotel.make_inc(2500, 978)
        fourth_inc_resp = Hotel.send_data(fourth_inc)
        assert fourth_inc_resp['de039'] == '00'
        reversal = Hotel.make_reversal(de007=init['de007'], de011=init['de011'])
        reversal_resp = Hotel.send_data(reversal)
        assert reversal_resp['de039'] == '00'
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        assert in_base[4]['accepted'] == 0
        assert in_base[4]['detail'] == 10
        assert in_base[3]['accepted'] == 0
        assert in_base[3]['detail'] == 11

    # Частичный реверсал на инкремент с ответом 05
    def test_partial_increment_decline(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        assert init['de039'] == '00'
        Hotel.de014 = '2307'
        first_inc = Hotel.make_inc(3000, 978)
        first_inc_resp = Hotel.send_data(first_inc)
        assert first_inc_resp['de039'] == '05'
        new_sum = 2000
        Hotel.de014 = card['card4']['de014']
        reversal = Hotel.make_partial_reversal(new_sum, de011=first_inc['data']['de011'],
                                               de007=first_inc['data']['de007'])
        reversal_resp = Hotel.send_data(reversal)
        assert reversal_resp['de039'] == '00'
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.2f}".format(new_sum * 0.01))
        assert in_base[1]['authvalue'] == 1.2
        assert in_base[1]['accepted'] == 1
        assert in_base[1]['detail'] == 0
        assert in_base[0]['accepted'] == 0
        assert in_base[0]['detail'] == 11

    # Частичный реверсал на инкрементную операцию, сумма меньше чем сумма в инкрементной операции, по 38 полю
    def test_partial_increment_sum_less_38(self):
        card = self.card_env
        Hotel = auth.HotelAuth(card['card4']['de002'], card['card4']['de014'], 120, 978, card['card4']['de035'])
        init = Hotel.send_data()
        first_inc = Hotel.make_inc(3000, 978)
        Hotel.send_data(first_inc)
        second_inc = Hotel.make_inc(2000, 978)
        second_inc_resp = Hotel.send_data(second_inc)
        new_sum = 1
        reversal = Hotel.make_partial_reversal(new_sum, de038=second_inc_resp['de038'])
        reversal['data']['de090'] = '000000000000000000000000000000000000000000'
        Hotel.send_data(reversal)
        in_base = dbquery.Dbquery.get_auth_trans6((Hotel.de037,))
        expected_summ = float("{:.2f}".format(new_sum * 0.01))
        for t6_auth in in_base[1:]:
            assert t6_auth['accepted'] == 1
            assert t6_auth['detail'] == 0
        assert in_base[0]['authvalue'] == expected_summ
        assert in_base[0]['accepted'] == 1
        assert in_base[0]['detail'] == 10