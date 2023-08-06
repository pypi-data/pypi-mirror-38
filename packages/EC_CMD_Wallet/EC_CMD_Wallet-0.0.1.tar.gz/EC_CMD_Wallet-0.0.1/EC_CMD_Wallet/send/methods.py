from ._btc import btc_send
from ._eth import eth_send


def send(currency:str, volume:float, fee:float, privateKey:str, to:str)->bool:
    """像目标发起转账.
    
    
    Args:
        currency (str): [description]
        volume (float): [description]
        fee (float): [description]
        privateKey (str): [description]
        to (str): [description]
    
    Returns:
        success (bool): 是否创建成功
    """

    if currency == "btc":
        result = btc_send(volume, fee, privateKey, to)
        url = f"https://blockchain.info/tx/{result}"
    elif currency == "eth":
        result = eth_send(volume, fee, privateKey, to)
        url = f"https://etherscan.io/tx/{result}"
    else:
        print("未知的货币")
        return False
    print("Here is the transaction ")
    print(url)
    return True
