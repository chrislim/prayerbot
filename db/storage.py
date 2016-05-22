#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

import os
import sqlite3
from labels import label_id

data = [
    {label_id: 12, "user_id": "1099770976753951", "description": "Potrzebuję modlitwy w intencji mojej mamy", "ts": 1412412331, "said": "no", "commiter_id": "1099770976753951", },
    {label_id: 13, "user_id": "1099770976753951", "description": "O powrót do zdrowia", "ts": 121312313, "said": "no", "commiter_id": "", },
    {label_id: 15, "user_id": "1209178385783730", "description": "O rozeznanie drogi", "ts": 121312312, "said": "no", "commiter_id": '', },
    {label_id: 16, "user_id": "10208414992228182", "description": "O Światowe Dni Młodzieży", "ts": 121312313, "said": "no", "commiter_id": "1209178385783730", },
    {label_id: 17, "user_id": "10208414992228182", "description": "W intencji Bogu wiadomej", "ts": 121312313, "said": "no", "commiter_id": "1099770976753951", },
    {label_id: 18, "user_id": "215380638847054", "description": "W intencji Bogu wiadomej", "ts": 121312313, "said": "yes", "commiter_id": '', },
]

cmd_create = """\
CREATE TABLE IF NOT EXISTS t_intent(
user_id text,
description text,
ts integer,
said text,
commiter_id text
)
"""

cmd_select = """\
SELECT %(label_name)s, * FROM t_intent\
%(where_clause)s
"""

cmd_insert = """\
INSERT INTO t_intent(
%(part_label)s\
user_id,
description,
ts,
said,
commiter_id
)
VALUES
(
%(part_value)s\
'%(user_id)s',
'%(description)s',
%(ts)d,
'%(said)s',
'%(commiter_id)s'
)
"""

db_file = 'intent.db'

def is_db_file():
    return os.path.isfile(db_file)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def fetch_from_db(id_value=None):
    if is_db_file():
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
        if id_value is None:
            where_clause = ''
        else:
            where_clause = ' WHERE %(label_name)s=%(label_value)d' % dict(
                label_name=label_id,
                label_value=id_value,
                )
        c = conn.cursor()
        cmd = cmd_select % dict(
            label_name=label_id,
            where_clause=where_clause,
            )
        data = c.execute(cmd)
    return data.fetchall()

def insert_row(data_line, conn=None):
    if conn is None:
        conn = sqlite3.connect(db_file)
        is_opened = 1
    else:
        is_opened = 0
    c = conn.cursor()
    if label_id in data_line:
        part_label = '%(label_name)s,\n' % dict(
            label_name=label_id,
            )
        part_value = '%(label_value)d,\n' % dict(
            label_value=data_line[label_id],
            )
    else:
        part_label = ''
        part_value = ''
    data_line.update(dict(
        part_label=part_label,
        part_value=part_value,
        ))
    cmd = cmd_insert % data_line
    c.execute(cmd)
    conn.commit()
    if is_opened:
        conn.close()

if not is_db_file():
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(cmd_create)
    if not fetch_from_db():
        for data_line in data:
            insert_row(data_line, conn=conn)
    conn.commit()

def fetch_history():
    data = fetch_from_db()
    return data
