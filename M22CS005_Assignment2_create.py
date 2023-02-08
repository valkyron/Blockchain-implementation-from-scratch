import sqlite3
import datetime

sqliteConnection = sqlite3.connect('M22CS005_blockchain.db')

cursr = sqliteConnection.cur()

cmd = """CREATE TABLE BLOCK (block_index INTEGER PRIMARY KEY,
                timestamp VARCHAR(50),
                proof INTEGER,
                prev_hash VARCHAR(256),
                transactions_hash VARCHAR(512),
                hashBlock VARCHAR(256)
                );"""

cursr.execute(cmd)

time = datetime.datetime.now()
timestamp = time.strftime("%d/%m/%Y, %H:%M:%S")
data = [(0, timestamp, 0, 0, 0, 0),]

cursr.executemany("""INSERT INTO BLOCK (block_index, timestamp, proof, prev_hash, transactions_hash, hashBlock) VALUES (?,?,?,?,?,?);""", data)
sqliteConnection.commit()


cmd = """CREATE TABLE TRANSACTIONS (block_index INTEGER, 
                sender VARCHAR(256),
                receiver VARCHAR(256),
                amount FLOAT, 
                timestamp VARCHAR(50));"""

cursr.execute(cmd)

cmd = """CREATE TABLE USERS (name VARCHAR(50),
                pvtKey VARCHAR(256),
                pubKey VARCHAR(256),
                address VARCHAR(256));"""

cursr.execute(cmd)

sqliteConnection.close()