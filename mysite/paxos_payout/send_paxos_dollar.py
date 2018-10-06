import web3 as w3
import os
import requests
import json
Infura_API_Key = '0fa94c53080547759661a8b3bdc1f63f'
os.environ['INFURA_API_KEY'] = Infura_API_Key
from web3.auto.infura import w3

decoding_string = 'teamkalsh'

# filename = 'teamkalsh'
# key_data = json.loads(open(filename,'r').read())
# private_key = w3.eth.account.decrypt(key_data,decoding_string)
#
# sender_address = str(w3.eth.account.privateKeyToAccount(private_key).address)

def retrieve_abi_from_contract_address(contract_address):

    ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='

    response = requests.get('%s%s'%(ABI_ENDPOINT, contract_address))
    response_json = response.json()
    abi_json = json.loads(response_json['result'])
    return (abi_json)

def load_contract(nifty_app_addres ='0x8e870d67f660d95d5be530380d0ec0bd388289e1'):
    nifty_app_address = w3.toChecksumAddress('0x8e870d67f660d95d5be530380d0ec0bd388289e1')
    #depending on app name, load abi and address
    Contract_abi = retrieve_abi_from_contract_address(nifty_app_address)
    # Contract_address = '0x06012c8cf97BEaD5deAe237070F9587f8E7A266d'
    #return contract object
    return(w3.eth.contract(address=nifty_app_address,abi=Contract_abi))

def prepare_paxos_dollar_tx(to_address, private_key, amount_to_send):
    contract = load_contract('0x8e870d67f660d95d5be530380d0ec0bd388289e1')
    #checksum addresses, just to be sure
    to_address = w3.toChecksumAddress(to_address)
    #grab nonce
    from_address = w3.toChecksumAddress(str(w3.eth.account.privateKeyToAccount(private_key).address))
    nonce = w3.eth.getTransactionCount(from_address)
    balance = w3.eth.getBalance(from_address)
    print(balance)
    #prepare transaction for transfer function
    #for now, gas limit is 1,000,000 and gas price is 3 Gwei
    amount = int(amount_to_send* 4485035922634800)
    print(amount)
    new_txn = {
    'to': to_address,
    'value': w3.toHex(amount),
    'gas': 21000,
    'gasPrice': w3.toWei('15','gwei'),
    'nonce': nonce,
    'chainId': 1
    }
    #sign transaction
    signed_txn = w3.eth.account.signTransaction(new_txn, private_key=private_key)
    #return signed transaction
    return (signed_txn)
    print(private_key)
