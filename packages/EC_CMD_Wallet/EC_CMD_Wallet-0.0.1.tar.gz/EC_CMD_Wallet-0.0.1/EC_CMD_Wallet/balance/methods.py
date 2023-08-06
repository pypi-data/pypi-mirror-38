from ._btc import btc_balance
from ._eth import eth_balance


def get_balance(address: str, private: bool, currency: str)->bool:
    """获取balance
    
    Args:
        address (str): 当private为true时指定私钥,为false时指定地址,注意私钥为不带`0x`的hex字符串
        private (bool): 指明address是私钥还是地址
        currency (str): 指明使用的货币
    
    Returns:
        success (bool): 获取balance是否成功
    """

    if currency == "btc":
        result = btc_balance(address, private)
    elif currency == "eth":
        result = eth_balance(address, private)
    else:
        print("未知的货币")
        return False

    print(f"{currency}:{result}")
    return True
