# encoding: utf8

import pandas as pd
import contextlib


@contextlib.contextmanager
def excel_write_context(file_name):
    try:
        writer = pd.ExcelWriter(file_name)
        yield writer
    finally:
        writer.save()


def pd_sql_to_excel(writer, conn, sql, sheet_name=u'Sheet1', index=False):
    df = pd.read_sql_query(sql, conn)
    df.to_excel(writer, sheet_name=sheet_name, index=False, encoding='utf8')
    writer.save()
