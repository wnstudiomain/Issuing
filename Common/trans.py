import datetime
import random
from Common.auth import Auth
import os
from os import environ as env
from Common.ssh_client import SSh as SSHClient


class Posting:
    VI_IP = env.get('INCOMING_VI_IP')
    VI_BIN_FOLDER = env.get('INCOMING_VI_BIN_FOLDER')
    VI_BIN_APP = env.get('INCOMING_VI_APP_NAME')
    POSTING_IP = env.get('POSTING_IP')
    POSTING_BIN_FOLDER = env.get('POSTING_BIN_FOLDER')
    POSTING_BIN_APP = env.get('POSTING_APP_NAME')
    PORT = env.get('SSH_PORT')
    USER = env.get('SSH_USER')
    VI_FILE_PATH = "/srv/data/IncomingVI/"

    def __init__(self, data):
        self.data = data

    @staticmethod
    def conv_date_to_settelment(data):
        y = str(data.year)
        day = data.strftime("%j").rjust(3, '0')
        return y + day

    def make_tc46_batch(self):
        for key, data in self.data.items():
            if data['de039'] is not None and data['de039'] != '05':
                transaction_code = '46'
                transaction_code_qualifier = '0'
                transaction_component_sequence_number = '0'
                destination_bin = '478530'
                source_bin = '000000'
                reporting_for_sre_identifier = '1000671142'
                rollup_to_sre_identifier = '3867074937'
                funds_transfer_sre_identifier = '3867074937'
                settlement_service_identifier = '080'
                settlement_currency_code = data['de051'] if data.get('de051') is not None else '978'
                clearing_currency_code = data['de051'] if data.get('de051') is not None else '978'
                business_mode = '2'
                no_data_indicator = ' '
                reserved = ' '
                report_group = 'V'
                report_subgroup = '4'
                report_identification_number = '120'
                report_identification_suffix = '  '
                settlement_date = self.conv_date_to_settelment(datetime.datetime.today())
                report_date = self.conv_date_to_settelment(datetime.datetime.today())
                noparse = '                 '
                business_transaction_type = '100'
                business_transaction_cycle = '1'
                reversal_indicator = 'N'
                return_indicator = 'N'
                noparse2 = '                              '
                summary_level = '10'
                noparse3 = '                                 0'
                currency_table_date = '       '
                first_count = '1'.zfill(15)
                second_count = '               '
                first_amount = data['de006'] if data.get('de006') is not None else '000000000000'
                second_amount = '000000000000000'
                second_amount_sign = '  '
                third_amount = data['de006'] if data.get('de006') is not None else '000000000000'
                noparse4 = '                                                                            '
                if data['de003'][0:2] == '26' or data['de003'][0:2] == 20:
                    first_amount_sign = 'CR'
                    third_amount_sign = 'CR'
                else:
                    first_amount_sign = 'DR'
                    third_amount_sign = 'DR'
                first = transaction_code + transaction_code_qualifier + transaction_component_sequence_number + destination_bin \
                        + source_bin + reporting_for_sre_identifier + rollup_to_sre_identifier + funds_transfer_sre_identifier \
                        + settlement_service_identifier + settlement_currency_code + clearing_currency_code + business_mode + no_data_indicator \
                        + reserved + report_group + report_subgroup + report_identification_number + report_identification_suffix \
                        + settlement_date + report_date + noparse + business_transaction_type + business_transaction_cycle + reversal_indicator \
                        + return_indicator + noparse2 + summary_level + noparse3
                second = transaction_code + transaction_code_qualifier \
                         + "1" + currency_table_date + first_count + second_count \
                         + first_amount + first_amount_sign + second_amount + second_amount_sign + third_amount + third_amount_sign + noparse4
                output = first + \
                         "\r\n" + second
                return output

    def make_tc5_batch(self):
        for key, data in self.data.items():
            if data['de039'] is not None and data['de039'] != '05':
                tr_code = {
                    '26': '26' if (data['mti'] == '0420') else '06',
                    '00': '25' if (data['mti'] == '0420') else '05',
                    '10': '25' if (data['mti'] == '0420') else '05',
                    '01': '25' if (data['mti'] == '0420') else '07',
                    '20': '26' if (data['mti'] == '0420') else '06',
                }
                tr_code_qualifier = {
                    '26': '2',
                    '00': '0',
                    '10': '1',
                    '01': '0',
                    '20': '0'
                }
                cpd = data['de037'][0:4]
                transaction_code = '06'
                acquirers_business_id = "00000000"
                acquirer_reference_number = f"745700010537053015{random.randint(10000, 99999)}"
                purchase_date = datetime.datetime.today().strftime("%m%d")
                destination_amount = data['de006'] if data.get('de006') is not None else '000000000000'
                destination_currency_code = data['de051'] if data.get('de051') is not None else '978'
                source_amount = data['de004'] if data.get('de004') is not None else '000000000000'
                source_currency_code = data['de049'] if data.get('de049') is not None else '978'
                merchant_name = data['de043'][0:25]
                merchant_city = data['de043'][25:38]
                merchant_country_code = data['de043'][-2:] + ' '
                merchant_zip_code = "03308"
                merchant_category_code = data['de018']
                merchant_state_province_code = "   "
                requested_payment_service = " "
                reserved01 = " "
                usage_code = data['de022'][3:4]
                authorization_code = data['de038']
                pos_terminal_capability = "5"
                cardholder_id_method = "1"
                collection_only_flag = " "
                pos_entry_mode = data['de022'][0:2]
                central_processing_date = cpd if cpd != '8259' else '0000'
                reimbursement_attribute = "B"
                chargeback_reference_number = "000000"
                card_acceptor_id = data['de042']
                terminal_id = data['de041']
                national_reimbursement_fee = "000000000000"
                mail_phone_electronic_commerce_and_payment_indicator = data['de060'][9:10] if data.get('de060')[9:10] is not None else ' '
                special_chargeback_indicator = " "
                interface_trace_number = Auth.pref37field()[0:4] + '00'
                acceptance_terminal_indicator = " "
                prepaid_card_indicator = " "
                service_development_field = " "
                avs_response_code = " "
                authorization_source_code = "V"
                purchase_identifier_format = " "
                account_selection = "0"
                instalment_payment_count = "  "
                purchase_identifier = "                         "
                cashback = "000000000"
                chip_condition_code = " "
                pos_environment = " "
                business_format_code = "SD"
                network_identification_code = "0000"
                contact_information = "                         "
                adjustment_processing_indicator = " "
                message_reason_code = "    "
                surcharge_amount = "00000000"
                surcharge_credit_debit_indicator = "  "
                visa_internal_use_only = "                "
                surcharge_amount_in_cardholder_billing_currency = "00000000"
                money_transfer_foreign_exchange_fee = "00000000"
                payment_account_reference = Auth.decode(data['de056']['01']['1']) if data.get('de056') is not None and data.get('de056').get('01') is not None and data.get('de056').get('01').get('1') is not None else "                             "
                token_requestor_id = Auth.decode(data['de123']['68']['3']) if data.get('de123') is not None and data.get('de123').get('68') is not None and data.get('de123').get('68').get('3') is not None else "           "
                transaction_identifier = data['de062']['2'] if data.get('de062') is not None and data.get('de062').get('2') is not None else f"3001633827{random.randint(10000, 99999)}"
                authorized_amount = data['de006'] if data.get('de006') is not None else '000000000000'
                authorization_currency_code = data['de051'] if data.get('de051') is not None else '978'
                authorization_response_code = data['de038']
                validation_code = "    "
                excluded_transaction_identifier_reason = " "
                crs_processing_code = " "
                chargeback_rights_indicator = "  "
                multiple_clearing_sequence_number = "00"
                multiple_clearing_sequence_count = "00"
                market_specific_authorization_data_indicator = " "
                total_authorized_amount = "000000000000"
                information_indicator = "N"
                merchant_telephone_number = "              "
                additional_data_indicator = " "
                merchant_volume_indicator = "  "
                electronic_commerce_goods_indicator = " "
                merchant_verification_value = "          "
                interchange_fee_amount = "000000000126040"
                interchange_fee_sign = "C"
                source_currency_to_base_currency_exchange_rate = "00000000"
                base_currency_to_destination_currency_exchange_rate = "00000000"
                optional_issuer_isa_amount = "000000000000"
                product_id = data['de062']['23'] if data.get('de062') is not None and data.get('de062').get('23') is not None else "F"
                program_id = "      "
                dynamic_currency_conversion_indicator = " "
                reserved1 = "     "
                token = Auth.decode(data['de123']['68']['1']) if data.get('de123') is not None and data.get('de123').get('68') is not None and data.get('de123').get('68').get('1') is not None else "0000000000000000"
                reserved2 = "  "
                cvv2_result_code = " "
                transaction_code = tr_code[data['de003'][0:2]] if data['de003'][0:2] in tr_code else '05'
                transaction_code_qualifier = tr_code_qualifier[data['de003'][0:2]] if data['de003'][
                                                                                      0:2] in tr_code_qualifier else '0'
                if data['de003'][0:2] == '11':
                    transaction_code = '15'
                    business_format_code = 'DF'
                    network_identification_code = '0002'
                first = transaction_code + transaction_code_qualifier + "0" + data[
                    'de002'] + "000Z  " + acquirer_reference_number + acquirers_business_id + purchase_date \
                        + destination_amount + destination_currency_code + source_amount + source_currency_code + merchant_name + merchant_city \
                        + merchant_country_code + merchant_category_code + merchant_zip_code + merchant_state_province_code + requested_payment_service + reserved01 + usage_code \
                        + "008N" + authorization_code \
                        + pos_terminal_capability + " " + cardholder_id_method + collection_only_flag + pos_entry_mode + central_processing_date \
                        + reimbursement_attribute
                second = transaction_code + transaction_code_qualifier + "1" + "            " + chargeback_reference_number + "                                                          " \
                         + card_acceptor_id + terminal_id + national_reimbursement_fee + mail_phone_electronic_commerce_and_payment_indicator + special_chargeback_indicator \
                         + interface_trace_number + acceptance_terminal_indicator + prepaid_card_indicator + service_development_field \
                         + avs_response_code + authorization_source_code + purchase_identifier_format + account_selection + instalment_payment_count \
                         + purchase_identifier + cashback + chip_condition_code + pos_environment
                if payment_account_reference == "                             " and token_requestor_id == "           ":
                    fourth = ""
                else:
                    fourth = transaction_code + transaction_code_qualifier + "4" + "          " + business_format_code + network_identification_code + contact_information \
                             + adjustment_processing_indicator + message_reason_code + surcharge_amount + surcharge_credit_debit_indicator \
                             + visa_internal_use_only + "                           " + surcharge_amount_in_cardholder_billing_currency \
                             + money_transfer_foreign_exchange_fee + payment_account_reference + token_requestor_id + "         "
                fifth = transaction_code + transaction_code_qualifier \
                        + "5" + transaction_identifier + authorized_amount + authorization_currency_code \
                        + authorization_response_code + validation_code + excluded_transaction_identifier_reason + crs_processing_code \
                        + chargeback_rights_indicator + multiple_clearing_sequence_number + multiple_clearing_sequence_count \
                        + market_specific_authorization_data_indicator + total_authorized_amount + information_indicator \
                        + " " + merchant_telephone_number \
                        + additional_data_indicator + merchant_volume_indicator + electronic_commerce_goods_indicator + merchant_verification_value \
                        + interchange_fee_amount + interchange_fee_sign + source_currency_to_base_currency_exchange_rate + base_currency_to_destination_currency_exchange_rate \
                        + optional_issuer_isa_amount + product_id + program_id + dynamic_currency_conversion_indicator + reserved1 + token \
                        + reserved2 + cvv2_result_code
                seventh = ""
                output = first + \
                         "\r\n" + second + \
                         "\r\n" + fourth + \
                         "\r\n" + fifth + \
                         "\r\n" + seventh
                return output

    def make_data_vi(self):
        batch = {
            'tcr5': self.make_tc46_batch(),
            'tcr46': self.make_tc5_batch()
        }
        return batch

    def make_posting(self):
        batch = {
            'tcr5': self.make_tc5_batch(),
            'tcr46': self.make_tc46_batch()
        }
        date = datetime.datetime.today().strftime("%d%m%y")
        cur_dir = os.path.join(os.path.dirname(__file__), '../posting/')
        name = f'EPIN.TXT.210127180001_{date}_{random.randint(10000, 99999)}'
        with open(cur_dir + '/EPIN.TXT_p1', 'r') as f1:
            p1 = f1.read()
        with open(cur_dir + '/EPIN.TXT_p2.1', 'r') as f2:
            p21 = f2.read()
        with open(cur_dir + '/EPIN.TXT_p2.2', 'r') as f3:
            p22 = f3.read()
        content = p1 + "\r\n" + batch['tcr5'] + p21 + "\r\n" + p22
        with open(cur_dir + name, 'w') as f:
            f.write(content)
        ssh_vi = SSHClient(self.VI_IP, self.PORT, self.USER)
        ssh_vi.scp_put_files(cur_dir + name, self.VI_FILE_PATH)
        ssh_vi.run_jar(self.VI_BIN_FOLDER, self.VI_BIN_APP)
        ssh_posting = SSHClient(self.POSTING_IP, self.PORT, self.USER)
        date_posting = datetime.datetime.today().strftime("%Y-%m-%d")
        ssh_posting.run_jar(self.POSTING_BIN_FOLDER, self.POSTING_BIN_APP, date_posting)