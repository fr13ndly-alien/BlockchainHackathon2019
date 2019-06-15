from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json

with open('/home/sean/web2py/web2py/applications/Certify/controllers/Certify.json') as f:
    abi = json.load(f)
    
w3 = Web3(HTTPProvider('https://testnet.tomochain.com'))
    
contract_address     =  ''
contract_address = Web3.toChecksumAddress(contract_address)
wallet_private_key   = ''

contract = w3.eth.contract(address = contract_address, abi = abi)

def store_results(_name, _address, _course, _status, _dateIssued, _grade):
    wallet_address = ''
    wallet_address = Web3.toChecksumAddress(wallet_address)

    #nonce = w3.eth.getTransactionCount(wallet_address)
    nonce = w3.eth.getTransactionCount(w3.eth.coinbase)

    txn_dict = contract.functions.chatsave(_username, _date, _hash).buildTransaction({
        'chainId': 89,
        'gas': 340000,
        'gasPrice': w3.toWei('40', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=wallet_private_key)

    result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.getTransactionReceipt(result)

    count = 0
    while tx_receipt is None and (count < 30):

        time.sleep(10)

        tx_receipt = w3.eth.getTransactionReceipt(result)

    return(tx_receipt)


    if tx_receipt is None:
        tx_receipt = "Failed"
        return(tx_receipt)

def check_hash(sessionId):   
    tx_receipt = contract.functions.checkhash(tokenId).call()
    return(tx_receipt)        

def tsend(username, date, hash):
    _username = str(username)
    _date = int(date)
    _hash = str(hash)
    _status = str(status)
    tx_receipt = store_results(_username, _date, _hash)
    return tx_receipt


def hashcheck(sessionId):
    sessionId = int(sessionId)
    tx_receipt = check_hash(sessionId)
    return tx_receipt
	
#examples:	
#hashcheck(0)
#tsend(An, 190420,0xAB346EfD106F)