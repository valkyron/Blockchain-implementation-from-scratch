# Blockchain-implementation-from-scratch

This code attempts to implement blockchain and it's base functionalities from sratch with SQLITE database in python.

SQLITE3 DATABASE TABLES:
1. BLOCK: Hold block data (timestamp, proof, prev_hash, transactions_hash, hash_block) index-wise
2. TRANSACTIONS: Holds all transaction data
3. USERS: Hols all users info (username, private key, public key, address)

The code contains 2 classes:
1. User: creates users with attributes public_key, private_key, address, signature, rand no.
2. Blockchain: creates blocks, maintains proof of work, replaces chain, checks validity of chain and more.

USER FUNCTIONS:
1. __init__: Initialize all characteristics and add user to SQL database
2. Signature: signs a transaction using user's private key

BLOCKCHAIN FUNCTIONS:
1. __init__: Initializes empty transactions, creates empty block, nodes and users
2. chain: returns blockchain which it retrieves from DB
3. get_previous_block: get previous block details
4. transactions_hash: get all transactions hash to be added to the block
5. hashBlock: return hash of the block
6. createBlock: create block and make relevant changes to TRANSACTION and BLOCK table in DB
7. proof_of_work = validates the miner's work and returns new_prof value
8. is_chain_valid: checks validity of chain by matching all blocks' 'previous hash' parameter with the hash of previous block, and verifying proof of work.
9. add_transaction: adding transaction (if first then adding genesis) to transactions array
10. identify: identify the username and return public address
11. add_node: add node to blockchain nodes list
12. add_user: add users to blockchain users list
13. spent_amount: check total spent amount
14. get_balance: get balance of specific user

APP ROUTING
1. mine_block
2. add_user
3. add_transaction
4. connect_node
5. replace_chain
6. wallet_balance

--------------------------------------------------------------------------------------------------------------------------------------------------------
QUERY ANSWERS:
import sqlite3

dbConnect = sqlite3.connect('M22CS005_blockchain.db')

cur = dbConnect.cursor()

1. Genesis transaction: find the (Genesis) block hash from the transaction hash.
 cur.execute("SELECT hashBlock FROM BLOCK WHERE block_index==(SELECT block_index FROM TRANSACTIONS WHERE sender==\"Genesis\");")
OUTPUT: ('fac35e67a286d8a3f48bb228d2e5b53b82b412ce20f3a169e77bc69a8a556496',)

2. Find the addresses and amounts of the transactions. 
 cur.execute("SELECT transactions_hash, amount from BLOCK INNER JOIN TRANSACTIONS ON BLOCK.block_index = TRANSACTIONS.block_index;")

3. Show the block information of the block with the hash address of (input the hash of the block).
 2303d4ad908c3ce6204ce081179341134f08464343f790df1c9b583752272389
 hash = input("What is the block hash?")
 script = "SELECT * from BLOCK WHERE BLOCK.hashBlock = (?);"
 cur.execute(script, (hash,))

4. Show the height of the most recent block stored.
cur.execute("SELECT MAX(block_index) FROM BLOCK;")

5. Show the most recent block stored. 
cur.execute("SELECT * FROM BLOCK WHERE block_index = (SELECT MAX(block_index) FROM BLOCK);")

6. The average number of transactions per block in the entire Bitcoin blockchain. 
cur.execute("SELECT COUNT(*) * 1.0 / COUNT(DISTINCT block_index) from TRANSACTIONS;")

7. Show a summary report of the transactions in the block with height 6 with two columns:
    #A. “Number of transactions”: numbers of transactions.
    #B. “Total input Bitcoins”: total inputs’ BTC of transactions.

cur.execute("SELECT COUNT(*), SUM(amount) from TRANSACTIONS GROUP BY block_index;")

rows = cur.fetchall()
for row in rows:
    print(row)


dbConnect.close()
