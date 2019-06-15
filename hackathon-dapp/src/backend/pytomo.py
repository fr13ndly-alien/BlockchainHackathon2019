from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
import json
import hashlib

with open('./abi.json') as f:
    abi = json.load(f)

# http address of provider, using ganache with following http address
w3 = Web3(HTTPProvider('http://127.0.0.1:8545'))

contract_address     =  '0xedD7E8971430b9e06c4bb8D1d738a3f3881d9199'
contract_address = Web3.toChecksumAddress(contract_address)
# private key of the account run smart contract
wallet_private_key   = '0x1295cdab3ce02af7d0be1559258f0888cf61341251407719fc5503081dfdc25e'

contract = w3.eth.contract(address = contract_address, abi = abi)

# Create document to push to Blockchain
def create_document (_ipfsAddress, _hashValue):
    # your wallet address - like account address
    wallet_address = '0x61f657bd80e0dd773ecc59bdc971e8a2b8c4226e'
    wallet_address = Web3.toChecksumAddress(wallet_address)
    print('\n- Wallet address checksum: ', wallet_address)
        
    nonce = w3.eth.getTransactionCount(wallet_address)
    #nonce = w3.eth.getTransactionCount(w3.eth.coinbase)

    print ("\n- transaction nonce: ", nonce)
        
    txn_dict = contract.functions.createDocument(_ipfsAddress, _hashValue).buildTransaction({
        'chainId': 1977, # default none: use for local net, see in truffle-config.js
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

def get_document(_creatorAddress):
    tx_recept = contract.functions.getDocument(_creatorAddress).call()
    return tx_recept #json file

crDoc = create_document("ipfs_address", "hash_value")
print ("\n\n- Ethereum smart contract create document: ", crDoc)