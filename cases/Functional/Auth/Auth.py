import pytest

from Common import auth, trans
from Common.dbquery import Dbquery as Query


def test_afd_120(card_env):
    card = card_env
    card_data = Query.get_intacccode_by_pan((card['card4']['de002'],))
    amount_check = 200
    formated_amount_check = float("{:.2f}".format(amount_check * 0.01))
    amount_advice = 994
    formated_amount_advice = float("{:.2f}".format(amount_advice * 0.01))
    otb = float("{:.2f}".format(Query.get_acc_otb(card_data)[0]))
    print(f"{otb} \n")
    expected_otb = round(otb - formated_amount_check - formated_amount_advice, 2)
    AFD = auth.AFD(card['card4']['de002'], card['card4']['de014'], amount_check, 978, card['card4']['de035'])
    response = AFD.send_data()
    advice = AFD.afd_advice(response['de038'], amount_advice)
    AFD.send_data(advice)
    new_otb = round(Query.get_acc_otb(card_data)[0], 2)
    print(new_otb)
    assert new_otb == expected_otb


@pytest.mark.parametrize("merchant_country_cod",
                         ["WM MORRISONS PETROL OP   BOLTON       GB",
                          "WM MORRISONS PETROL OP   BOLTON       TR",
                          "WM MORRISONS PETROL OP   BOLTON       US"
                          ])
def test_afd_block_1_value(card_env, merchant_country_cod):
    card = card_env
    AFD = auth.AFD(card['card4']['de002'], card['card4']['de014'], 100, 826, card['card4']['de035'])
    AFD.de043 = merchant_country_cod
    response = AFD.send_data()
    assert response['de039'] == '05'


@pytest.mark.parametrize("merchant_country_cod",
                         ["WM MORRISONS PETROL OP   BOLTON       GB",
                          "WM MORRISONS PETROL OP   BOLTON       TR",
                          "WM MORRISONS PETROL OP   BOLTON       US",
                          "WM MORRISONS PETROL OP   BOLTON       LV"
                          ])
@pytest.mark.parametrize("amount", [99, 101])
def test_afd_block_1_value_not_1(card_env, merchant_country_cod, amount):
    card = card_env
    AFD = auth.AFD(card['card4']['de002'], card['card4']['de014'], amount, 978, card['card4']['de035'])
    AFD.de043 = merchant_country_cod
    response = AFD.send_data()
    assert response['de039'] == '00'


@pytest.mark.parametrize("ccy", ['978', '826', '840'])
def test_afd_block_1_different_currency(card_env, ccy):
    card = card_env
    AFD = auth.AFD(card['card4']['de002'], card['card4']['de014'], 100, ccy, card['card4']['de035'])
    AFD.de049 = ccy
    response = AFD.send_data()
    assert response['de039'] == '05'


@pytest.mark.parametrize("mcc", ["5812", "6011", "3618"])
@pytest.mark.parametrize("ccy", ['826', '840'])
def test_afd_not_block_mcc(card_env, mcc, ccy):
    card = card_env
    CPToken = auth.CPToken(card['card4']['de002'], card['card4']['de014'], 100, ccy, card['card4']['de035'])
    CPToken.de018 = mcc
    response = CPToken.send_data()
    assert response['de039'] == '00'

