from EC_CMD_Wallet.const import WEB3
from eth_account import Account


def eth_balance(address, private):
    if private:
        acct = Account.privateKeyToAccount(address)
        address = acct.address
    result = WEB3.fromWei(WEB3.eth.getBalance(address), 'ether')
    return result
