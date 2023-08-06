#!/usr/bin/env python3
from datetime import datetime

import pandas


def get_cell_value(xls, row_index, column_index):
    """
    :param xls: target xls
    :param row_index: row index in xls
    :param column_index: column index in xls
    :return: value at coordinate or None if cell is empty
    """
    try:
        value = xls.iloc[row_index, column_index]
        return None if pandas.isnull(value) else value
    except IndexError:
        return None


def get_horizontal_field_value(xls, row_index, description_index, fields_count=1, description=None, partial_match=False):
    """
    There are values in the xls that have descriptions in one cell and the value to the left, this function
    is a helper in those cases
    :param xls: target pandas xls
    :param row_index: self explanatory
    :param description_index: column index where the description string of the "field" exists
    :param fields_count: if there are more then one fields, horizontal, to concatenate
    :param description: if provided, will try to fully or partially match target cell content with this
    :param partial_match: choose if the description matching is partially or not
    :return: cell, concatenated cells or None if all cells are empty
    """
    if description:
        actual_description = get_cell_value(xls, row_index, description_index)
        if not actual_description:
            raise ValueError("empty cell at coordinate: {}:{}".format(row_index, description_index))
        mismatch = False
        if partial_match:
            if description not in actual_description:
                mismatch = True
        else:
            if description != actual_description:
                mismatch = True
        if mismatch:
            raise ValueError("Mismatch between expected description and actual description: \"{}\" != \"{}\""
                             .format(description, actual_description))
    output = []
    for i in range(1, fields_count + 1, 1):
        cell_value = get_cell_value(xls, row_index, description_index + i)
        if cell_value is not None:
            output.append(cell_value)
    if not output:
        return None
    return ' '.join(v for v in output)


def get_cell_datetime(xls, row_index, column_index, date_format):
    value = get_cell_value(xls, row_index, column_index)
    if value is not None:
        return datetime.strptime(value, date_format)
    return None


from .raiffeisen import RaiffeisenStatement, ClientData, Transaction, AccountData
