from bit.network import NetworkAPI, satoshi_to_currency_cached
from bit import Key


def btc_balance(address, private):
    if private:
        s_k = Key.from_hex(address)
        address = s_k.address
    btc_balance = NetworkAPI.get_balance(address)
    return satoshi_to_currency_cached(btc_balance, "btc")
