from bit.network import NetworkAPI, satoshi_to_currency_cached
from bit import Key


def btc_send(volume, fee, privateKey, to):
    s_k = Key.from_hex(privateKey)
    if fee:
        result = s_k.send([(to, volume, 'btc')], fee=fee)
    else:
        result = s_k.send([(to, volume, 'btc')])
    return result
