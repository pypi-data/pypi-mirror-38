#!/usr/bin/env python3

from .context import bankreader
import unittest
from mock import patch
import pandas
import os
from datetime import datetime

from bankreader.romania import get_cell_value, get_horizontal_field_value, get_cell_datetime
from bankreader.romania import RaiffeisenStatement, ClientData, AccountData


class RomaniaTesting(unittest.TestCase):
    def setUp(self):
        self.statements_folder = os.path.join(os.path.dirname(__file__), 'statements')
        self.def_statement = "Extras_de_cont_12345678_20012018_31012018.xls"

    def to_date(self, date_time, date_format):
        return datetime.strptime(date_time, date_format)

    def get_statement_path(self, xls_file_name):
        return os.path.join(self.statements_folder, xls_file_name)

    def get_statement(self, xls_file_name):
        return RaiffeisenStatement(self.get_statement_path(xls_file_name))

    def test_file_name_parser_valid(self):
        file_name = "Extras_de_cont_12345678_01092018_30092018.xls"
        output = RaiffeisenStatement._parse_statement_file_name(file_name)
        expected = {
            "account_number": "12345678",
            "start_generation_time": self.to_date("01092018", RaiffeisenStatement.FILE_NAME_DATE_FORMAT),
            "end_generation_time": self.to_date("30092018", RaiffeisenStatement.FILE_NAME_DATE_FORMAT)
        }

        self.assertDictEqual(output, expected)

    def test_file_name_parser_invalid_time(self):
        file_name = "Extras_de_cont_ValueError.xls"
        self.assertRaises(ValueError, RaiffeisenStatement._parse_statement_file_name, file_name)

    def test_file_name_parser_invalid_underline_count(self):
        file_name = "Extras_.xls"
        self.assertRaises(ValueError, RaiffeisenStatement._parse_statement_file_name, file_name)

    def test_file_name_parser_invalid_name(self):
        file_name = "_de_cont_12345678_01092018_30092018.xls"
        self.assertRaises(ValueError, RaiffeisenStatement._parse_statement_file_name, file_name)

    def test_parse_transaction_date_range(self):
        input_value = "de la 22/01/2018 la 31/01/2018"
        expected_from = datetime(2018, 1, 22, 0, 0)
        expected_to = datetime(2018, 1, 31, 0, 0)
        self.assertListEqual(RaiffeisenStatement._parse_transaction_date_range(input_value), [expected_from, expected_to])

    def test_parse_transaction_date_range_invalid(self):
        input_value = "de la 22/01/2018 la"
        self.assertRaises(ValueError, RaiffeisenStatement._parse_transaction_date_range, input_value)

    def test_init(self):
        RaiffeisenStatement(self.get_statement_path(self.def_statement))

    def test_get_value_valid(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertEqual(get_cell_value(xls, 0, 0), "Data generare extras:")

    def test_get_value_invalid(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertEqual(get_cell_value(xls, 4242, 4242), None)

    def test_get_horizontal_field_value_valid(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertEqual(get_horizontal_field_value(xls, 0, 0), "03.02.2018")

    def test_get_horizontal_field_value_valid_none(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertEqual(get_horizontal_field_value(xls, 4242, 4242), None)

    def test_get_horizontal_field_value_multiple_valid(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertEqual(get_horizontal_field_value(xls, 5, 0, fields_count=4),
                         'BL.-,SC.-,ET.- Some address 2 Some county ROMANIA')

    def test_get_horizontal_field_value_multiple_description_valid(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertEqual(get_horizontal_field_value(xls, 5, 0, fields_count=4, description="Adresa:"),
                         'BL.-,SC.-,ET.- Some address 2 Some county ROMANIA')

    def test_get_horizontal_field_value_multiple_description_invalid(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertRaises(ValueError, get_horizontal_field_value, xls, 5, 0, fields_count=4, description="ValueError")

    def test_get_datetime_valid(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        expected_time = datetime(2018, 2, 3, 0, 0)
        self.assertEqual(get_cell_datetime(xls, 0, 1, "%d.%m.%Y"), expected_time)

    def test_get_datetime_invalid_index(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertEqual(get_cell_datetime(xls, 4242, 4242, "%d.%m.%Y"), None)

    def test_get_datetime_invalid_format(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        self.assertRaises(ValueError, get_cell_datetime, xls, 0, 1, "ValueError")

    def test_get_transaction_date_range_valid(self):
        def my_init(self, xls_path):
            self.xls = pandas.read_excel(xls_path)

        with patch.object(RaiffeisenStatement, "__init__", my_init):
            statement = RaiffeisenStatement(self.get_statement_path(self.def_statement))

            expected_from = datetime(2018, 1, 22, 0, 0)
            expected_to = datetime(2018, 1, 31, 0, 0)
            self.assertListEqual(statement._get_transaction_date_range(), [expected_from, expected_to])

    def test_client_data_init(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        ClientData(xls)

    def test_client_data_type(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        client_data = ClientData(xls)
        self.assertIsInstance(client_data.currency, str)
        self.assertIsInstance(client_data.account_type, str)
        self.assertIsInstance(client_data.iban, str)
        self.assertIsInstance(client_data.bank_unit, str)
        self.assertIsInstance(client_data.bic_code, str)
        self.assertIsInstance(client_data.client_number, str)
        self.assertIsInstance(client_data.client_address, str)

    def test_client_data_str(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        expected = "<|abarbatei|BL.-,SC.-,ET.- Some address 2 Some county ROMANIA|" \
                   "1234567890|RZBAAAAA|RAIFFEISEN BANK S.A. AGENT.City Some street|" \
                   "RO69RZBR1234567890123456|curent|LEI|>"
        client_data = ClientData(xls)

        self.assertEqual(str(client_data), expected)

    def test_account_data_init(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        AccountData(xls)

    def test_account_data_type(self):
        xls = pandas.read_excel(self.get_statement_path(self.def_statement))
        account_data = AccountData(xls)

        self.assertIsInstance(account_data.expenses, float)
        self.assertIsInstance(account_data.final_balance, float)
        self.assertIsInstance(account_data.income, float)
        self.assertIsInstance(account_data.initial_balance, float)

    def test_process_transactions_len(self):
        def my_init(self, xls_path):
            self.xls = pandas.read_excel(xls_path)

        with patch.object(RaiffeisenStatement, "__init__", my_init):
            statement = RaiffeisenStatement(self.get_statement_path(self.def_statement))
            transactions = statement._process_transactions()
            self.assertEqual(len(transactions), 5)

    def test_process_transactions_valid_one(self):
        def my_init(self, xls_path):
            self.xls = pandas.read_excel(xls_path)

        with patch.object(RaiffeisenStatement, "__init__", my_init):
            statement = RaiffeisenStatement(self.get_statement_path(self.def_statement))
            transactions = statement._process_transactions()
            expected_registration_date = datetime(2018, 1, 22, 0, 0)
            expected_finalization_date = datetime(2018, 1, 22, 0, 0)
            expected_raw_desciption = 'Payment 1 |Card nr. XXXX XXXX XXXX 1234 |Data utilizarii cardului 18/01/2018'
            trans = transactions[0]
            self.assertEqual(trans.registration_date, expected_registration_date)
            self.assertEqual(trans.finalization_date, expected_finalization_date)
            self.assertEqual(trans.expense_amount, 100.0)
            self.assertEqual(trans.income_amount, None)
            self.assertEqual(trans.raw_description, expected_raw_desciption)
            self.assertEqual(trans.payment_order_id, None)
            self.assertEqual(trans.beneficiary_financial_code, None)
            self.assertEqual(trans.final_adjudicator, None)
            self.assertEqual(trans.final_beneficiary, None)
            self.assertEqual(trans.involved_party.is_payment(), True)
            self.assertEqual(trans.card_usage_date, datetime(2018, 1, 18, 0, 0))
            self.assertEqual(trans.description, 'Payment 1 ')
            self.assertEqual(trans.extra_data, 'Card nr. XXXX XXXX XXXX 1234 ')

    def test_process_transactions_valid_two(self):
        def my_init(self, xls_path):
            self.xls = pandas.read_excel(xls_path)

        with patch.object(RaiffeisenStatement, "__init__", my_init):
            statement = RaiffeisenStatement(self.get_statement_path(self.def_statement))
            transactions = statement._process_transactions()
            expected_registration_date = datetime(2018, 1, 22, 0, 0)
            expected_finalization_date = datetime(2018, 1, 22, 0, 0)
            expected_raw_description = 'OPH/unknown stuff |stuff |stuff'
            trans = transactions[3]
            self.assertEqual(trans.registration_date, expected_registration_date)
            self.assertEqual(trans.finalization_date, expected_finalization_date)
            self.assertEqual(trans.expense_amount, None)
            self.assertEqual(trans.income_amount, 100.0)
            self.assertEqual(trans.raw_description, expected_raw_description)
            self.assertEqual(trans.payment_order_id, 123)
            self.assertEqual(trans.beneficiary_financial_code, '12345678')
            self.assertEqual(trans.final_adjudicator, None)
            self.assertEqual(trans.final_beneficiary, None)
            self.assertEqual(trans.involved_party.name, "FIRMA SRL")
            self.assertEqual(trans.involved_party.bank_name, "SOMEBANK ROMANIA")
            self.assertEqual(trans.involved_party.account_number, "RO77CITI1234567123456789")
            self.assertEqual(trans.card_usage_date, None)
            self.assertEqual(trans.description, expected_raw_description)
            self.assertEqual(trans.extra_data, None)


if __name__ == "__main__":
    unittest.main()
