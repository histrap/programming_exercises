from flask import Flask
import json
import sqlite3

#globals
app = Flask(__name__)

#functions

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_conn(name='bitcoin'):
    conn = sqlite3.connect("%s.db" %(name))
    conn.row_factory = dict_factory
    return conn

def get_blocks(conn, count=-1):
  #if count == -1, get all
  sql = "SELECT * from blocks"

  if count != -1:
    sql += " LIMIT %d" %(count)

  c = conn.cursor()
  c.execute(sql)
  return c.fetchall()


@app.route('/')
@app.route('/blocks')
def blocks():
  db_conn = get_db_conn()
  blocks = get_blocks(db_conn)
  return json.dumps(blocks)

if __name__ == '__main__':
  app.run()