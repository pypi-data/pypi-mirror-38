#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

import logging
import ntpath
import re
from datetime import datetime

import pandas

from bankreader.romania import get_cell_value, get_horizontal_field_value, get_cell_datetime


class Transaction:
    # these are row indexes
    REGISTRATION_DATE_INDEX = 0
    FINALIZATION_DATE_INDEX = 1
    EXPENSE_AMOUNT_INDEX = 2
    INCOME_AMOUNT_INDEX = 3
    PAYMENT_ORDER_ID_INDEX = 4
    BENEFICIARY_FINANCIAL_CODE_INDEX = 5
    FINAL_ADJUDICATOR_INDEX = 6
    FINAL_BENEFICIARY_INDEX = 7
    INVOLVED_PARTY_NAME_INDEX = 8
    INVOLVED_PARTY_BANK_NAME_INDEX = 9
    INVOLVED_PARTY_ACCOUNT_INDEX = 10
    DESCRIPTION_INDEX = 11

    def __init__(self, registration_date, finalization_date, income_amount, expense_amount, raw_description,
                 payment_order_id=None, beneficiary_financial_code=None, final_adjudicator=None, final_beneficiary=None,
                 involved_party_name=None, involved_party_bank_name=None, involved_party_account=None):

        self.registration_date = registration_date
        self.finalization_date = finalization_date
        self.income_amount = income_amount
        self.expense_amount = expense_amount
        self.raw_description = raw_description
        self.payment_order_id = payment_order_id
        self.beneficiary_financial_code = beneficiary_financial_code
        self.final_adjudicator = final_adjudicator
        self.final_beneficiary = final_beneficiary

        self.involved_party = BankAccount(name=involved_party_name,
                                          bank_name=involved_party_bank_name,
                                          account_number=involved_party_account)

        # A transaction can not be simultaneously be an income and an outcome, amount is the sum regardless of the case
        if self.income_amount is not None:
            self.amount = self.income_amount
            self.is_income = True
        elif self.expense_amount is not None:
            self.amount = self.expense_amount
            self.is_income = False
        else:
            raise ValueError("income amount and expenses amount can not be simultaneously None")

        self.card_usage_date = None
        self.extra_data = None
        self.description = self.raw_description

        parts = self.raw_description.split("|")
        if len(parts) == 2:
            # unknown bank stuff |my personal nice description YYY.mm.dd
            self.extra_data = parts[0]
            self.description = parts[1]
        elif len(parts) == 3:
            if 'cardului' in parts[2]:
                # Nice transaction in some city |Card nr. XXXX XXXX XXXX YYYY |Data utilizarii cardului dd/mm/YY
                self.description = parts[0]
                self.extra_data = parts[1]
                self.card_usage_date = datetime.strptime(parts[2][-10:], "%d/%m/%Y")

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__dict__)


class BankAccount:
    def __init__(self, name, bank_name, account_number):
        self.name = name
        self.bank_name = bank_name
        self.account_number = account_number

    def is_payment(self):
        return all(v is None for v in [self.account_number, self.bank_name, self.account_number])

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__dict__)


class ClientData:

    NAME_LOC = {"r": 4, "c": 0}
    CLIENT_ADDRESS_LOC = {"r": 5, "c": 0, 'cnt': 4}
    CLIENT_NUMBER_LOC = {"r": 6, "c": 0}
    BIC_CODE_LOC = {"r": 7, "c": 0}
    BANK_UNIT_LOC = {"r": 8, "c": 0, 'cnt': 3}

    IBAN_LOC = {"r": 10, "c": 0}
    ACCOUNT_TYPE_LOC = {"r": 10, "c": 2}
    CURRENCY_LOC = {"r": 10, "c": 4}

    @staticmethod
    def _get_correct_value(xls, name_dict):
        count = name_dict.get('cnt', 1)
        description = name_dict.get('dsc', None)
        return get_horizontal_field_value(xls, name_dict['r'], name_dict['c'],
                                          fields_count=count, description=description)

    def __init__(self, xls):
        self.client_name = self._get_correct_value(xls, self.NAME_LOC)
        self.client_address = self._get_correct_value(xls, self.CLIENT_ADDRESS_LOC)
        self.client_number = self._get_correct_value(xls, self.CLIENT_NUMBER_LOC)
        self.bic_code = self._get_correct_value(xls, self.BIC_CODE_LOC)
        self.bank_unit = self._get_correct_value(xls, self.BANK_UNIT_LOC)
        self.iban = self._get_correct_value(xls, self.IBAN_LOC)
        self.account_type = self._get_correct_value(xls, self.ACCOUNT_TYPE_LOC)
        self.currency = self._get_correct_value(xls, self.CURRENCY_LOC)

    def __str__(self):
        return "|".join(["<", self.client_name, self.client_address, self.client_number,
                         self.bic_code, self.bank_unit, self.iban, self.account_type,
                         self.currency, ">"])


class AccountData:
    ACCOUNT_ROW_DESCRIPTION_INDEX = 12
    ACCOUNT_ROW_VALUE_INDEX = ACCOUNT_ROW_DESCRIPTION_INDEX + 1

    def __init__(self, xls):
        self.initial_balance = float(get_cell_value(xls, self.ACCOUNT_ROW_VALUE_INDEX, 0))
        self.expenses = float(get_cell_value(xls, self.ACCOUNT_ROW_VALUE_INDEX, 1))
        self.income = float(get_cell_value(xls, self.ACCOUNT_ROW_VALUE_INDEX, 2))
        self.final_balance = float(get_cell_value(xls, self.ACCOUNT_ROW_VALUE_INDEX, 3))


class RaiffeisenStatement:

    FILE_NAME_DATE_FORMAT = "%d%m%Y"
    TRANSACTION_DATE_FORMAT = "%d/%m/%Y"
    STATEMENT_GENERATION_DATE_FORMAT = "%d.%m.%Y"

    REGISTRATION_DATE_RANGE_TRANSACTION_COLUMN_INDEX = 1

    # row indexes
    STATEMENT_GENERATION_DATE_DESCRIPTION_INDEX = 0
    ENTRY_ROW_DESCRIPTION_INDEX = 15
    ENTRY_ROW_VALUE_START_INDEX = ENTRY_ROW_DESCRIPTION_INDEX + 2

    def __init__(self, xls_path, verbose=False):
        """
        :param xls_path:
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.disabled = not verbose
        self.xls_path = xls_path
        self.transactions_range = None
        self.account_number = None
        self.start_period = None
        self.end_period = None
        self.client = None
        self.account = None
        self.transactions = list()
        self.xls = pandas.read_excel(xls_path)

        statement_file_generation_data = self._parse_statement_file_name(xls_path)
        try:
            self.account_number = statement_file_generation_data.get('account_number')
            self.start_period = statement_file_generation_data.get('start_generation_time')
            self.end_period = statement_file_generation_data.get('end_generation_time')
        except ValueError:
            self.logger.warning("could not retrieve account number and statement generation period from file name")

        self.generation_date = datetime.strptime(
            get_horizontal_field_value(self.xls, 0, self.STATEMENT_GENERATION_DATE_DESCRIPTION_INDEX),
            RaiffeisenStatement.STATEMENT_GENERATION_DATE_FORMAT)
        try:
            self.transactions_range = self._get_transaction_date_range()
        except ValueError:
            self.logger.warning("could not retrieve transaction range")

        self.client = ClientData(self.xls)
        self.account = AccountData(self.xls)
        self.transactions = self._process_transactions()

    def _process_transactions(self):
        transactions = list()
        entry_row_index = self.ENTRY_ROW_VALUE_START_INDEX - 1

        while True:
            entry_row_index += 1
            if pandas.isnull(self.xls.iloc[entry_row_index, 0]):
                break

            registration_date = get_cell_datetime(self.xls, entry_row_index,
                                                  Transaction.REGISTRATION_DATE_INDEX,
                                                  self.TRANSACTION_DATE_FORMAT)

            finalization_date = get_cell_datetime(self.xls, entry_row_index,
                                                  Transaction.FINALIZATION_DATE_INDEX,
                                                  self.TRANSACTION_DATE_FORMAT)

            expense_amount = get_cell_value(self.xls, entry_row_index, Transaction.EXPENSE_AMOUNT_INDEX)
            income_amount = get_cell_value(self.xls, entry_row_index, Transaction.INCOME_AMOUNT_INDEX)
            payment_order_id = get_cell_value(self.xls, entry_row_index, Transaction.PAYMENT_ORDER_ID_INDEX)
            beneficiary_financial_code = get_cell_value(self.xls, entry_row_index,
                                                        Transaction.BENEFICIARY_FINANCIAL_CODE_INDEX)
            final_adjudicator = get_cell_value(self.xls, entry_row_index, Transaction.FINAL_ADJUDICATOR_INDEX)
            final_beneficiary = get_cell_value(self.xls, entry_row_index, Transaction.FINAL_BENEFICIARY_INDEX)
            involved_party_name = get_cell_value(self.xls, entry_row_index, Transaction.INVOLVED_PARTY_NAME_INDEX)
            involved_party_bank_name = get_cell_value(self.xls, entry_row_index,
                                                      Transaction.INVOLVED_PARTY_BANK_NAME_INDEX)
            involved_party_account = get_cell_value(self.xls, entry_row_index,
                                                    Transaction.INVOLVED_PARTY_ACCOUNT_INDEX)
            raw_description = get_cell_value(self.xls, entry_row_index, Transaction.DESCRIPTION_INDEX)

            transactions.append(Transaction(
                registration_date=registration_date,
                finalization_date=finalization_date,
                expense_amount=expense_amount,
                income_amount=income_amount,
                payment_order_id=payment_order_id,
                beneficiary_financial_code=beneficiary_financial_code,
                final_adjudicator=final_adjudicator,
                final_beneficiary=final_beneficiary,
                involved_party_name=involved_party_name,
                involved_party_bank_name=involved_party_bank_name,
                involved_party_account=involved_party_account,
                raw_description=raw_description
            ))

        return transactions

    def _get_transaction_date_range(self):
        value = str(self.xls.columns[self.REGISTRATION_DATE_RANGE_TRANSACTION_COLUMN_INDEX])
        return self._parse_transaction_date_range(value)

    @staticmethod
    def _parse_statement_file_name(xls_path):
        """
        Some (almost none) description can be found here (pages 16 and 17):
        https://www.raiffeisen.ro/wps/wcm/connect/211686be-6c69-4023-897b-a9b8f3763498/Ghid-de-utilizare-Raiffeisen-Online-IMM.pdf?MOD=AJPERES&CVID=

        Old format: Extras_<account_number>_<statement_date>.xls
        New format: Extras_de_cont_<account_number>_<chosen_start_date>_<chosen_end_date>.xls
        eg. Extras_de_cont_12345678_01012018_20012018.xls
        :return: dict with keys/values
            "account_number"
            "start_generation_time"
            "end_generation_time"
        """
        xls_file_name = ntpath.basename(xls_path).strip(".xls")

        if xls_file_name.startswith("Extras_") is False:
            raise ValueError(".xls name is not a valid bank extras, must be Extras_<other>, got: {}"
                             .format(xls_file_name))

        parts = xls_file_name.split("_")
        account_number, from_date, to_date = parts[-3:]
        start_generation_time = datetime.strptime(from_date, RaiffeisenStatement.FILE_NAME_DATE_FORMAT)
        end_generation_time = datetime.strptime(to_date, RaiffeisenStatement.FILE_NAME_DATE_FORMAT)

        return {
            "account_number": account_number,
            "start_generation_time": start_generation_time,
            "end_generation_time": end_generation_time
        }

    @staticmethod
    def _parse_transaction_date_range(value):
        date_regex = re.compile(r'(?:0[1-9]|[12][0-9]|3[01])[- /.](?:0[1-9]|1[012])[- /.](?:19|20)\d\d]?')

        from_date, to_date = date_regex.findall(value)
        from_date = datetime.strptime(from_date, RaiffeisenStatement.TRANSACTION_DATE_FORMAT)
        to_date = datetime.strptime(to_date, RaiffeisenStatement.TRANSACTION_DATE_FORMAT)
        return [from_date, to_date]
