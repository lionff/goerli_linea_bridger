from web3 import Web3
import random
import json
import time

with open("privates.txt", "r") as f:
    keys_list = [row.strip() for row in f if row.strip()]

w3 = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth_goerli'))

CONTRACT_ABI = json.load(open('abi_linea.json'))
CONTRACT_ADDRESS = w3.to_checksum_address('0x70bad09280fd342d02fe64119779bc1f0791bac2')

linea_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

for KEY in keys_list:
    account = w3.eth.account.from_key(KEY)
    address = account.address
    print(address)

    eth_quantity_to_bridge = 1  # на все акки полетит по 1 эфиру - можно зарандомить сумму в диапазоне раскомментив строку ниже и закомментив эту

    # eth_quantity_to_bridge = random.uniform(0.1,1) # рандомное количество эфира для бриджа в диапазоне от 0.1 до 1

    eth_quantity = w3.to_wei(eth_quantity_to_bridge, 'ether')

    contract_address_l2 = address
    value = eth_quantity
    calldata = b''
    fee = 1000000000000000

    tx = linea_contract.functions.sendMessage(
        address,
        fee,
        calldata,
    ).build_transaction({
        'from': address,
        'maxFeePerGas': int(w3.eth.gas_price + (w3.eth.gas_price * 0.25)),
        'maxPriorityFeePerGas': w3.eth.max_priority_fee,
        'value': value,
        'nonce': w3.eth.get_transaction_count(address)
    })

    signed_transaction = w3.eth.account.sign_transaction(tx, KEY)
    txn = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    print(f"Transaction: https://goerli.etherscan.io/tx/{txn.hex()}")
    time.sleep(15)
