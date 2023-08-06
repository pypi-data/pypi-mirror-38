import time
from EC_CMD_Wallet.const import WEB3
from eth_account import Account


def eth_send(volume, fee, privateKey, to):
    key = privateKey if privateKey.startswith("0x") else "0x"+privateKey
    acct = Account.privateKeyToAccount(privateKey)
    address = acct.address
    value = WEB3.toWei(volume, 'ether')
    if not fee:
        fee = 0.0002
    gas = 25000
    gas_limit = WEB3.toWei(fee, 'ether')
    gasPrice = int(gas_limit / gas)
    nonce = WEB3.eth.getTransactionCount(address)
    transaction_dict = {
        'chainId': 1,
        'to': to,
        'value': value,
        'gas': gas,
        'gasPrice': gasPrice,
        'nonce': nonce
    }
    signed_txn = Account.signTransaction(transaction_dict, key)
    WEB3.eth.sendRawTransaction(signed_txn.rawTransaction)
    result = WEB3.toHex(WEB3.sha3(signed_txn.rawTransaction))
    return result
