import pytest

from Common import auth, trans


@pytest.fixture
def get_card(card_env, request):
    return card_env[request.param]


@pytest.mark.parametrize("get_card", ["card2", "card3"], indirect=True)
@pytest.mark.parametrize("merchant_country_cod",
                         ["FUMINOR033-A. SAHAROVA 20RIGA         GB", ])
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
    aq_trans_data = trans.get_data_trans_from_aq(data_mult[3]['de037'])
    assert t1.arn == aq_trans_data['acquirer_reference_number']

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
    t1 = trans.Posting(data_mult)
    t1.make_posting()
    aq_trans_data = trans.get_data_trans_from_aq(data_mult[3]['de037'])
    assert t1.arn == aq_trans_data['acquirer_reference_number']
