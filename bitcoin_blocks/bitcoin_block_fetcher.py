import requests
import json
import sqlite3
import time

def get_latest_block(url):
    r = requests.get(url)

    if r.status_code != 200:
        raise "Error getting latest transaction: %d" %(r.status)

    latest_transaction = json.loads(r.text)
    return latest_transaction

def write_block_to_db(conn, block):
    c = conn.cursor()
    try:
        c.execute("INSERT INTO blocks VALUES('%s', '%d', %d, %d)" %(block['hash'], block['time'], block['block_index'], block['height']))
    except sqlite3.IntegrityError:
        pass
    except Exception as e:
        raise e
    conn.commit()

def get_db_conn(name='bitcoin'):
    conn = sqlite3.connect("%s.db" %(name))
    return conn

def create_tables(conn):
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS blocks (hash text primary key, timestamp INTEGER, block_index INTEGER, height INTEGER)")
    conn.commit()

'''
To do:
    Write a function def get_max_block to fetch the latest block i.e. the most recent block
'''

def print_blocks(conn):
    '''
    To do
        1. Instead of unix timestamp in seconds, print actual date. i.e. instead of 1598456000
            print 2020-08-26T15:33:20+00:00
    '''
    c = conn.cursor()
    c.execute("SELECT * FROM blocks")
    for row in c.fetchall():
        print row

def main():
    url = "https://blockchain.info/latestblock"
    sleep_duration = 10
    db_conn = get_db_conn()
    create_tables(db_conn)
    while True:
        block = get_latest_block(url)
        write_block_to_db(db_conn, block)
        print "Blocks: "
        print_blocks(db_conn)
        print "Sleeping for %d seconds" %(sleep_duration)
        time.sleep(sleep_duration)

if __name__ == '__main__':
    main()
