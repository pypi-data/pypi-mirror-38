# encoding: utf8

import pandas as pd
from py_utils.excel import excel_write_context


FILE_NAME = 'test-excel.xlsx'


def test_excel_write_context():
    with excel_write_context(FILE_NAME) as writer:
        assert isinstance(writer, pd.ExcelWriter)
