from secrets import token_urlsafe
from eth_account import Account


def eth_new():
    rkey = token_urlsafe(10)
    acct = Account.create(rkey)
    addr = acct.address
    privKey = bytes(acct.privateKey).hex()
    return {
        "privateKey": privKey,
        "address": addr
    }
