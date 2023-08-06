from ._btc import btc_new
from ._eth import eth_new


def new(currency:str)->bool:
    """创建一个账户密码对
    
    Args:
        currency (str): 指定哪种货币
    
    Returns:
        success (bool): 是否创建成功
    """
    if currency == "btc":
        result = btc_new()
    elif currency == "eth":
        result = eth_new()
    else:
        print("未知的货币")
        return False
    for k, v in result.items():
        print(f"{k}:{v}")
    return True
