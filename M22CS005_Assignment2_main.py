# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse

import binascii
import Crypto
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import sqlite3


# Part 1 - Creating a user

class User:  
    def __init__(self,name):
        random_number = Crypto.Random.new().read
        self.name = name
        self.key = RSA.generate(1024,random_number)
        self.pvtKey = self.key.export_key("PEM")
        self.pubKey = self.key.publickey().export_key("OpenSSH")
        self.address = hashlib.sha256(str(self.pubKey).encode()).hexdigest()
        self.sign = PKCS1_v1_5.new(self.pvtKey)
        
        dbConnect = sqlite3.connect('M22CS005_blockchain.db')
        
        cur = dbConnect.cur()

        data = [(name, self.pvtKey, self.pubKey, self.address),]

        cur.executemany("""INSERT INTO USERS (name, pvtKey, pubKey, address) VALUES (?,?,?,?);""", data)

        dbConnect.commit()
        
        dbConnect.close()

    def signature(self):
        pvtKey = self.sender.pvtKey
        sign = PKCS1_v1_5.new(pvtKey)
        hsh = SHA.new(str(self.transaction(len(self.transactions)))).encode('utf0')
        return binascii.hexlify(sign.sign(hsh)).decode('ascii')




# Part 2 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.transactions = []
        self.createBlock(proof = 1, prev_hash = '0')
        self.nodes = set()
        self.users = []
        
        
    def chain(self):
        dbConnect = sqlite3.connect('M22CS005_blockchain.db')
        cur = dbConnect.cur()
        cur.execute("""SELECT * FROM transactions INNER JOIN block ON block.block_index = transactions.block_index;""")

        rows = cur.fetchall()
        chain = []
        for row in rows:
            chain.append ({'index': row[0],
                     'timestamp': row[6],
                     'proof': row[7],
                     'prev_hash': row[8],
                     'transactions': {'sender':row[1],
                                     'receiver':row[2],
                                     'amount': row[3],
                                     'timestamp': row[4]}
                     })
        return chain

    def get_previous_block(self):
        dbConnect = sqlite3.connect('M22CS005_blockchain.db')
        
        cur = dbConnect.cur()
        
        cur.execute("""SELECT * FROM BLOCK where block_index=(select max(block_index) from block);""")
        index = cur.fetchall()
        dbConnect.close()
        return index        

    def transactions_hash(self,block):
        ls = []
        for i in block['transactions']:
            ls.append(self.hash(i))
        return ls  
    
    def hashBlock(self,block):
        return self.hash(block)
    
    def createBlock(self, proof, prev_hash):
        time = datetime.datetime.now()
               
        index = self.get_previous_block()
        index = index[0][0] + 1
        timestamp = time.strftime("%d/%m/%Y, %H:%M:%S")
        
        block = {'index': index,
                 'timestamp': timestamp,
                 'proof': proof,
                 'prev_hash': prev_hash,
                 'transactions': self.transactions,
                 'transactions_hash':[],
                 'hashBlock':[]
                 }
        hash_trans = str(self.transactions_hash(block))
        block['transactions_hash'].append(hash_trans)
        hashBlock = str(self.hashBlock(block))
        block['hashBlock'].append(hashBlock)
        dbConnect = sqlite3.connect('M22CS005_blockchain.db')
        cur = dbConnect.cur()
        
        data = [(index, timestamp, proof, prev_hash, hash_trans, hashBlock),]

        cur.executemany("""INSERT OR REPLACE INTO BLOCK (block_index, timestamp, proof, prev_hash, transactions_hash, hashBlock) VALUES (?,?,?,?,?,?);""", data)
        
        dbConnect.commit()
        
        for i in self.transactions:
            sender = i['sender']
            receiver = i['receiver']
            amount = float(i['amount'])
            time = i['time']
            
            data = [(index, sender, receiver, amount, time),]
            
            cur.executemany("INSERT OR REPLACE INTO TRANSACTIONS (block_index, sender, receiver, amount, timestamp) VALUES (?,?,?,?,?);""", data)
            
            dbConnect.commit()
        
        dbConnect.close()
          
        self.transactions = [] 
        
        #self.chain.append(block)
        #block['_id'] = block['index']
        #self.replace_chain()
        return block

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['prev_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def identify(self, strg):
        pub_add = ""
        dbConnect = sqlite3.connect('M22CS005_blockchain.db')
        cur = dbConnect.cur()

        cur.execute("""SELECT * FROM users;""")

        rows = cur.fetchall()

        for row in rows:
            if row[0] == strg:
                pub_add = row[2]
            
        dbConnect.close()
        
        return pub_add
            
    def add_transaction(self, sender, receiver, amount):
        if sender == "Genesis":
            sender = "Genesis"
        else:
            sender = self.identify(sender)
        #print(sender)
        #print(self.identify(receiver))
        time = datetime.datetime.now()
        self.transactions.append({'sender': str(sender),
                                 'receiver': str(self.identify(receiver)),
                                 'amount': amount,
                                 'time': time.strftime("%d/%m/%Y, %H:%M:%S")})
        
        previous_block = self.get_previous_block()
        return previous_block[0][0] + 1
    
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def add_user(self, users):
        self.users.append(json['users'])
        return True
    
    
    def spent_amount(self, sender):
        balance = 0
        dbConnect = sqlite3.connect('M22CS005_blockchain.db')
        cur = dbConnect.cur()

        cur.execute("""SELECT * FROM transactions;""")

        rows = cur.fetchall()

        for row in rows:
            if row[1] == sender:
                balance += row[3]
            
        dbConnect.close()
        return balance

    def get_balance(self, sender):
        balance = 0
        sender = str(self.identify(sender))
        #print(sender)
        
        dbConnect = sqlite3.connect('M22CS005_blockchain.db')
        cur = dbConnect.cur()

        cur.execute("""SELECT * FROM transactions;""")

        rows = cur.fetchall()

        for row in rows:
            if row[2] == sender:
                balance += row[3]
            
        dbConnect.close()
        
        #print(balance , self.spent_amount(sender))
        net_balance = balance - self.spent_amount(sender)
        return net_balance


# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
# Creating an address for the node on Port 5001
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block[0][2]
    proof = blockchain.proof_of_work(previous_proof)
    prev_hash = previous_block[0][4]
    #blockchain.add_transaction(sender = node_address, receiver = 'LV', amount = 1)
    block = blockchain.createBlock(proof, prev_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'prev_hash': block['prev_hash'],
                'transactions_hash': block['transactions_hash'],
                'hashBlock': block['hashBlock']}
    #block['transactions']=[]
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    previous_block = blockchain.get_previous_block()
    length = previous_block[0][0]
    response = {'chain': blockchain.chain(),
                'length': length}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


# Adding a new user to the blockchain
@app.route('/add_user', methods = ['POST'])
def add_user():
    json = request.get_json()
    user_keys = json.get('user')
    if user_keys is None:
        return 'User name or amount missing', 400
    index = User(json['user'])
    #index.name = json['users']  
    blockchain.users.append(index)
    response = {'message': f'New User added name - {index.pubKey}'}
    return jsonify(response), 201


# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    #print(json['sender'])
    #balance = blockchain.get_balance(json['sender'])
    #print(balance)
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    if json['sender'] == 'Genesis':
        index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
        response = {'message': f'Genesis transaction will be added to Block {index}'}
    elif blockchain.get_balance(json['sender']) >= float(json['amount']):
        index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
        response = {'message': f'This transaction will be added to Block {index}'}
    else:
        response = {'message': 'This transaction can not be done, Insufficient Balance'}
    return jsonify(response), 201

# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200

@app.route('/wallet_balance', methods = ['POST'])
def wallet_balance():
    json = request.get_json()
    user_keys = json.get('user')
    if user_keys is None:
        return 'User name or amount missing', 400
    balance = blockchain.get_balance(json['user'])
    response = {'message': f'The wallet balance of the user is {balance}'}
    return jsonify(response), 201

# Running the app
app.run(host = '0.0.0.0', port = 5004)