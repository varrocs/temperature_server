
import sqlite3
import datetime
import os

DB='tempereratures.sqlite'

def _check_db():
    if not os.path.isfile(DB):
        conn = sqlite3.connect(DB)
        conn.execute("""CREATE TABLE data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TIMESTAMP,
            temperature FLOAT,
            humidity FLOAT
        )""")
        conn.commit()
        conn.close()


def _save(t, h):
    _check_db()
    now = datetime.datetime.now()
    conn = sqlite3.connect(DB)
    conn.execute('INSERT INTO data VALUES (?, ?, ?, ?)', (None, now, t, h))
    conn.commit()
    conn.close()

def last_n(n):
    _check_db()
    conn = sqlite3.connect(DB, detect_types=sqlite3.PARSE_DECLTYPES)
    result = [ {'date':row[1], 'temperature':row[2], 'humidity':row[3]} for row in conn.execute('SELECT * FROM data ORDER BY time DESC LIMIT ?', (n,) ) ]
    print(result)
    conn.close()
    return result

def on_data(d):
    try:
        temperature=float(d[0])
        humidity=float(d[1])
        _save(temperature, humidity)
    except Exception as e:
        print(e)


def do_test():
    on_data((11.0, 40.0))
    on_data((12.0, 35.0))
    on_data((13.0, 30.0))
    on_data((14.00, 20.0))
    on_data((15.0, 10.0))
    on_data((16.0, 5.5))

    print(last_n(2))
    print("*"*30)
    print(last_n(10))
