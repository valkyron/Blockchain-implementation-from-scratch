# Blockchain-implementation-from-scratch

README.TXT
Assignment - INTRO TO BLOCKCHAIN
Name - Devansh Kaushik
Roll No. - M22CS005

This code solves the assignment questions completely with saving data in the SQLITE database in python.

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

----------------------------------------------------------------------------------------------------------------------------------------------------------------
QUERY ANSWERS:
import sqlite3

dbConnect = sqlite3.connect('M22CS005_blockchain.db')

cur = dbConnect.cursor()

#1. Genesis transaction: find the (Genesis) block hash from the transaction hash.
 cur.execute("SELECT hashBlock FROM BLOCK WHERE block_index==(SELECT block_index FROM TRANSACTIONS WHERE sender==\"Genesis\");")
OUTPUT: ('fac35e67a286d8a3f48bb228d2e5b53b82b412ce20f3a169e77bc69a8a556496',)




2. Find the addresses and amounts of the transactions. 
 cur.execute("SELECT transactions_hash, amount from BLOCK INNER JOIN TRANSACTIONS ON BLOCK.block_index = TRANSACTIONS.block_index;")

OUTPUT:
("['adab22bef9353208da1e8e0466f5135b347702f2bb9cdc715312e7f432398248', 'd447f43cc0aee0b3a7262eac97d06eea735ade315be2e7e40ee794798e911c48', 'b7d16e77bb960d8691fe73bccd0216d59d475a6d94e899f8656be1d44c34d8fc', '30b6715332621d4f9dce3fe14825932357c6e90311f8ccae424c490e91d7f437', '2647bc898450b961285a42b47c71aff0c54e545f01c9a38b1d98a32b5d59e64f']", 3500.0)
 ("['adab22bef9353208da1e8e0466f5135b347702f2bb9cdc715312e7f432398248', 'd447f43cc0aee0b3a7262eac97d06eea735ade315be2e7e40ee794798e911c48', 'b7d16e77bb960d8691fe73bccd0216d59d475a6d94e899f8656be1d44c34d8fc', '30b6715332621d4f9dce3fe14825932357c6e90311f8ccae424c490e91d7f437', '2647bc898450b961285a42b47c71aff0c54e545f01c9a38b1d98a32b5d59e64f']", 2000.0)
 ("['adab22bef9353208da1e8e0466f5135b347702f2bb9cdc715312e7f432398248', 'd447f43cc0aee0b3a7262eac97d06eea735ade315be2e7e40ee794798e911c48', 'b7d16e77bb960d8691fe73bccd0216d59d475a6d94e899f8656be1d44c34d8fc', '30b6715332621d4f9dce3fe14825932357c6e90311f8ccae424c490e91d7f437', '2647bc898450b961285a42b47c71aff0c54e545f01c9a38b1d98a32b5d59e64f']", 4000.0)
 ("['adab22bef9353208da1e8e0466f5135b347702f2bb9cdc715312e7f432398248', 'd447f43cc0aee0b3a7262eac97d06eea735ade315be2e7e40ee794798e911c48', 'b7d16e77bb960d8691fe73bccd0216d59d475a6d94e899f8656be1d44c34d8fc', '30b6715332621d4f9dce3fe14825932357c6e90311f8ccae424c490e91d7f437', '2647bc898450b961285a42b47c71aff0c54e545f01c9a38b1d98a32b5d59e64f']", 500.0)
 ("['adab22bef9353208da1e8e0466f5135b347702f2bb9cdc715312e7f432398248', 'd447f43cc0aee0b3a7262eac97d06eea735ade315be2e7e40ee794798e911c48', 'b7d16e77bb960d8691fe73bccd0216d59d475a6d94e899f8656be1d44c34d8fc', '30b6715332621d4f9dce3fe14825932357c6e90311f8ccae424c490e91d7f437', '2647bc898450b961285a42b47c71aff0c54e545f01c9a38b1d98a32b5d59e64f']", 250.0)
 ("['6a6969497d7fc4cd751ee0fe04c5eeb5a3ee6aa1f4b42519070db4a79cd0eb94', '8a541a44f416b19530ddf88d5c588f20ff5ec4aff8fed1c68a340e6e44029cb2', '3fcc2993d1c71548af41777eef0fc7007f7e9ef149ac7ad0b8a541483038bdcd', '1f5cfedf7bc4becd52be2a90bb6b32c5afdf84b0966f2a669c1bd037634765d4', '8f99a8316f84fa908d7e34585f903fcd77dcc1fed799e35e2da862e4599b655a']", 250.0)
 ("['6a6969497d7fc4cd751ee0fe04c5eeb5a3ee6aa1f4b42519070db4a79cd0eb94', '8a541a44f416b19530ddf88d5c588f20ff5ec4aff8fed1c68a340e6e44029cb2', '3fcc2993d1c71548af41777eef0fc7007f7e9ef149ac7ad0b8a541483038bdcd', '1f5cfedf7bc4becd52be2a90bb6b32c5afdf84b0966f2a669c1bd037634765d4', '8f99a8316f84fa908d7e34585f903fcd77dcc1fed799e35e2da862e4599b655a']", 250.0)
 ("['6a6969497d7fc4cd751ee0fe04c5eeb5a3ee6aa1f4b42519070db4a79cd0eb94', '8a541a44f416b19530ddf88d5c588f20ff5ec4aff8fed1c68a340e6e44029cb2', '3fcc2993d1c71548af41777eef0fc7007f7e9ef149ac7ad0b8a541483038bdcd', '1f5cfedf7bc4becd52be2a90bb6b32c5afdf84b0966f2a669c1bd037634765d4', '8f99a8316f84fa908d7e34585f903fcd77dcc1fed799e35e2da862e4599b655a']", 250.0)
 ("['6a6969497d7fc4cd751ee0fe04c5eeb5a3ee6aa1f4b42519070db4a79cd0eb94', '8a541a44f416b19530ddf88d5c588f20ff5ec4aff8fed1c68a340e6e44029cb2', '3fcc2993d1c71548af41777eef0fc7007f7e9ef149ac7ad0b8a541483038bdcd', '1f5cfedf7bc4becd52be2a90bb6b32c5afdf84b0966f2a669c1bd037634765d4', '8f99a8316f84fa908d7e34585f903fcd77dcc1fed799e35e2da862e4599b655a']", 250.0)
 ("['6a6969497d7fc4cd751ee0fe04c5eeb5a3ee6aa1f4b42519070db4a79cd0eb94', '8a541a44f416b19530ddf88d5c588f20ff5ec4aff8fed1c68a340e6e44029cb2', '3fcc2993d1c71548af41777eef0fc7007f7e9ef149ac7ad0b8a541483038bdcd', '1f5cfedf7bc4becd52be2a90bb6b32c5afdf84b0966f2a669c1bd037634765d4', '8f99a8316f84fa908d7e34585f903fcd77dcc1fed799e35e2da862e4599b655a']", 250.0)
 ("['45316142333d58df662be24ba93e241807a9fcbc8e3077774f51c5112bcc0cc0', 'd2a9223421d33d409ae7f71a74d50b4fc80c99e1a5d7c28f3ba5569ca9101698', '3b211d37df3fa673c4f1dfa0818ff12cdfd404c673f861f7dbd161cd75475a16', '814d155083781b0b4cd249a8b8133f582b2a8a8a083daf0a7359209041d0a84d']", 250.0)
 ("['45316142333d58df662be24ba93e241807a9fcbc8e3077774f51c5112bcc0cc0', 'd2a9223421d33d409ae7f71a74d50b4fc80c99e1a5d7c28f3ba5569ca9101698', '3b211d37df3fa673c4f1dfa0818ff12cdfd404c673f861f7dbd161cd75475a16', '814d155083781b0b4cd249a8b8133f582b2a8a8a083daf0a7359209041d0a84d']", 250.0)
# ("['45316142333d58df662be24ba93e241807a9fcbc8e3077774f51c5112bcc0cc0', 'd2a9223421d33d409ae7f71a74d50b4fc80c99e1a5d7c28f3ba5569ca9101698', '3b211d37df3fa673c4f1dfa0818ff12cdfd404c673f861f7dbd161cd75475a16', '814d155083781b0b4cd249a8b8133f582b2a8a8a083daf0a7359209041d0a84d']", 250.0)
 ("['45316142333d58df662be24ba93e241807a9fcbc8e3077774f51c5112bcc0cc0', 'd2a9223421d33d409ae7f71a74d50b4fc80c99e1a5d7c28f3ba5569ca9101698', '3b211d37df3fa673c4f1dfa0818ff12cdfd404c673f861f7dbd161cd75475a16', '814d155083781b0b4cd249a8b8133f582b2a8a8a083daf0a7359209041d0a84d']", 60.0)
 ("['92f6cdf0f5495155c79f54fec6996ea0fc3190e77942f0b7300502987e4c8a4e', '6a3e30f70e31cf3f7c1d4201066a9e3c05d0509efd20bcfd950c2bc37e8a2298', '93e63cd71c0463fee671d74fee8ae370174811d35213181b5d48e49e47fc12bc', '63cacd26bf7d4a60bbc88d2e6b00064f928d792e96ae5c5c6b33bea8fc4d891d']", 600.0)
 ("['92f6cdf0f5495155c79f54fec6996ea0fc3190e77942f0b7300502987e4c8a4e', '6a3e30f70e31cf3f7c1d4201066a9e3c05d0509efd20bcfd950c2bc37e8a2298', '93e63cd71c0463fee671d74fee8ae370174811d35213181b5d48e49e47fc12bc', '63cacd26bf7d4a60bbc88d2e6b00064f928d792e96ae5c5c6b33bea8fc4d891d']", 1200.0)
 ("['92f6cdf0f5495155c79f54fec6996ea0fc3190e77942f0b7300502987e4c8a4e', '6a3e30f70e31cf3f7c1d4201066a9e3c05d0509efd20bcfd950c2bc37e8a2298', '93e63cd71c0463fee671d74fee8ae370174811d35213181b5d48e49e47fc12bc', '63cacd26bf7d4a60bbc88d2e6b00064f928d792e96ae5c5c6b33bea8fc4d891d']", 600.0)
 ("['92f6cdf0f5495155c79f54fec6996ea0fc3190e77942f0b7300502987e4c8a4e', '6a3e30f70e31cf3f7c1d4201066a9e3c05d0509efd20bcfd950c2bc37e8a2298', '93e63cd71c0463fee671d74fee8ae370174811d35213181b5d48e49e47fc12bc', '63cacd26bf7d4a60bbc88d2e6b00064f928d792e96ae5c5c6b33bea8fc4d891d']", 400.0)
 ("['b6357ec02645755bcc0c41d0e90625d0b8beb9b7e6f81796963692217b677a2f', '9fa033068544d7f34d89051c375c7fd6ca959f3bd510554c51e002027c39c0a1', '5b2f1b203d47b153dcf42830f1a42af996cedf5ebfb769030e3c99d7fdf1e4a4', '3e0f7bb8fce329f751befc983acccaddcfb15a4d45783298397603e553126062', 'c7ac272a149ecc07d5cf96a998482f37ecbcdc76cb56bea96e14322951c01ce5']", 400.0)
 ("['b6357ec02645755bcc0c41d0e90625d0b8beb9b7e6f81796963692217b677a2f', '9fa033068544d7f34d89051c375c7fd6ca959f3bd510554c51e002027c39c0a1', '5b2f1b203d47b153dcf42830f1a42af996cedf5ebfb769030e3c99d7fdf1e4a4', '3e0f7bb8fce329f751befc983acccaddcfb15a4d45783298397603e553126062', 'c7ac272a149ecc07d5cf96a998482f37ecbcdc76cb56bea96e14322951c01ce5']", 400.0)
 ("['b6357ec02645755bcc0c41d0e90625d0b8beb9b7e6f81796963692217b677a2f', '9fa033068544d7f34d89051c375c7fd6ca959f3bd510554c51e002027c39c0a1', '5b2f1b203d47b153dcf42830f1a42af996cedf5ebfb769030e3c99d7fdf1e4a4', '3e0f7bb8fce329f751befc983acccaddcfb15a4d45783298397603e553126062', 'c7ac272a149ecc07d5cf96a998482f37ecbcdc76cb56bea96e14322951c01ce5']", 250.0)
 ("['b6357ec02645755bcc0c41d0e90625d0b8beb9b7e6f81796963692217b677a2f', '9fa033068544d7f34d89051c375c7fd6ca959f3bd510554c51e002027c39c0a1', '5b2f1b203d47b153dcf42830f1a42af996cedf5ebfb769030e3c99d7fdf1e4a4', '3e0f7bb8fce329f751befc983acccaddcfb15a4d45783298397603e553126062', 'c7ac272a149ecc07d5cf96a998482f37ecbcdc76cb56bea96e14322951c01ce5']", 50.0)
 ("['b6357ec02645755bcc0c41d0e90625d0b8beb9b7e6f81796963692217b677a2f', '9fa033068544d7f34d89051c375c7fd6ca959f3bd510554c51e002027c39c0a1', '5b2f1b203d47b153dcf42830f1a42af996cedf5ebfb769030e3c99d7fdf1e4a4', '3e0f7bb8fce329f751befc983acccaddcfb15a4d45783298397603e553126062', 'c7ac272a149ecc07d5cf96a998482f37ecbcdc76cb56bea96e14322951c01ce5']", 50.0)





3. Show the block information of the block with the hash address of (input the hash of the block).
 2303d4ad908c3ce6204ce081179341134f08464343f790df1c9b583752272389
 hash = input("What is the block hash?")
 script = "SELECT * from BLOCK WHERE BLOCK.hashBlock = (?);"
 cur.execute(script, (hash,))

OUTPUT:
(6, '10/11/2022, 18:02:23', 48191, "['45316142333d58df662be24ba93e241807a9fcbc8e3077774f51c5112bcc0cc0', 'd2a9223421d33d409ae7f71a74d50b4fc80c99e1a5d7c28f3ba5569ca9101698', '3b211d37df3fa673c4f1dfa0818ff12cdfd404c673f861f7dbd161cd75475a16', '814d155083781b0b4cd249a8b8133f582b2a8a8a083daf0a7359209041d0a84d']", "['92f6cdf0f5495155c79f54fec6996ea0fc3190e77942f0b7300502987e4c8a4e', '6a3e30f70e31cf3f7c1d4201066a9e3c05d0509efd20bcfd950c2bc37e8a2298', '93e63cd71c0463fee671d74fee8ae370174811d35213181b5d48e49e47fc12bc', '63cacd26bf7d4a60bbc88d2e6b00064f928d792e96ae5c5c6b33bea8fc4d891d']", '2303d4ad908c3ce6204ce081179341134f08464343f790df1c9b583752272389')





4. Show the height of the most recent block stored.
cur.execute("SELECT MAX(block_index) FROM BLOCK;")

OUTPUT:
 (7, )





5. Show the most recent block stored. 
cur.execute("SELECT * FROM BLOCK WHERE block_index = (SELECT MAX(block_index) FROM BLOCK);")

OUTPUT:
(7, '10/11/2022, 18:06:08', 19865, "['92f6cdf0f5495155c79f54fec6996ea0fc3190e77942f0b7300502987e4c8a4e', '6a3e30f70e31cf3f7c1d4201066a9e3c05d0509efd20bcfd950c2bc37e8a2298', '93e63cd71c0463fee671d74fee8ae370174811d35213181b5d48e49e47fc12bc', '63cacd26bf7d4a60bbc88d2e6b00064f928d792e96ae5c5c6b33bea8fc4d891d']", "['b6357ec02645755bcc0c41d0e90625d0b8beb9b7e6f81796963692217b677a2f', '9fa033068544d7f34d89051c375c7fd6ca959f3bd510554c51e002027c39c0a1', '5b2f1b203d47b153dcf42830f1a42af996cedf5ebfb769030e3c99d7fdf1e4a4', '3e0f7bb8fce329f751befc983acccaddcfb15a4d45783298397603e553126062', 'c7ac272a149ecc07d5cf96a998482f37ecbcdc76cb56bea96e14322951c01ce5']", '1fd11af79d79307f112bec7d884042809e84fe5ceacf1ec5f0b63b9bbfbdd2ab')





6. The average number of transactions per block in the entire Bitcoin blockchain. 
cur.execute("SELECT COUNT(*) * 1.0 / COUNT(DISTINCT block_index) from TRANSACTIONS;")

OUTPUT
(4.6,)


7. Show a summary report of the transactions in the block with height 6 with two columns:
    #A. “Number of transactions”: numbers of transactions.
    #B. “Total input Bitcoins”: total inputs’ BTC of transactions.


cur.execute("SELECT COUNT(*), SUM(amount) from TRANSACTIONS GROUP BY block_index;")

OUTPUT
(5, 10250.0)
(5, 1250.0)
(4, 810.0)
(4, 2800.0)
(5, 1150.0)

rows = cur.fetchall()
for row in rows:
    print(row)


dbConnect.close()
