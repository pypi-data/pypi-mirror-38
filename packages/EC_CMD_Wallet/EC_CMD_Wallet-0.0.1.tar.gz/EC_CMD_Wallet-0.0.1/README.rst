EC_CMD_Wallet
===============================
* version: 0.0.1
* status: dev
* author: hsz
* email: hsz1273327@gmail.com


Desc
--------------------------------
一个超简单的命令行加密货币钱包,支持btc和eth,硬分叉完后视情况添加bch的支持

keywords: wallet


Feature
----------------------
* 完全无状态,不保存任何用户信息,用户自己保存私钥地址这类信息
* 支持查看balance,新建一个私钥地址对以及指定账户进行转账


Example
-------------------------------
.. code:: shell

    ecw -h

Install
--------------------------------
- ``python -m pip install EC_CMD_Wallet``


Documentation
--------------------------------
`Documentation on Readthedocs <https://finaceinfo.github.io/EC-CMD-Wallet/>`_.


TODO
-----------------------------------
* 支持erc20代币
* 视情况支持bch
