from bit import Key


def btc_new():
    nk = Key()
    privKey = nk.to_hex()
    addr = nk.address
    return {
        "privateKey": privKey,
        "address": addr
    }
