#!/usr/bin/env python
import sys
import argparse
from .new import new
from .balance import get_balance
from .send import send


def new_cmd(args):
    kwargs = {
        "currency": args.currency
    }
    new(**kwargs)


def get_balance_cmd(args):
    kwargs = {
        "address": args.address,
        "private": False,
        "currency": args.currency
    }
    if args.private:
        kwargs.update({
            "private": True
        })
    get_balance(**kwargs)


def send_cmd(args):
    kwargs = {
        "volume": args.volume,
        "fee": None,
        "currency": args.currency,
        "privateKey": args.privateKey,
        "to": args.to
    }
    if args.fee:
        kwargs.update({
            "fee": args.fee
        })
    send(**kwargs)


def parser_args(params):
    """[summary]
    解析命令行参数.

    Args:
        params ([type]): 要解析的参数
    """

    parser = argparse.ArgumentParser(
        prog='ecw',
        description='简易钱包',
        epilog='支持btc,eth'
    )
    parser.set_defaults(func=lambda x: parser.print_help())

    subparsers = parser.add_subparsers()

    new_parsers = subparsers.add_parser(
        "new", aliases=["N"], help="创建一个私钥/地址对")
    new_parsers.add_argument(
        "currency", type=str, help="货币对应的链", choices=['btc', 'eth'], default="btc")
    new_parsers.set_defaults(func=new_cmd)

    balance_parsers = subparsers.add_parser(
        "balance", aliases=["B"], help="查看余额")
    balance_parsers.add_argument(
        "address", type=str, help="查看对应地址的余额")
    balance_parsers.add_argument(
        "-c", "--currency", type=str, help="查看的货币名", choices=['btc', 'eth'], default="btc")
    balance_parsers.add_argument(
        "-p", "--private", action='store_true', help="查看的地址是否是私钥")
    balance_parsers.set_defaults(func=get_balance_cmd)

    send_parsers = subparsers.add_parser(
        "send", aliases=["T"], help="转账")
    send_parsers.add_argument(
        "volume", type=float, help="转账的量")
    send_parsers.add_argument(
        "-f", "--fee", type=float, help="指定使用多少手续费用于转账")
    send_parsers.add_argument(
        "-c", "--currency", type=str, help="指定转账的货币名", choices=['btc', 'eth'], default="btc")
    send_parsers.add_argument(
        "-p", "--privateKey", type=str, required=True, help="从对应私钥上转账")
    send_parsers.add_argument(
        "-t", "--to", type=str, required=True, help="转账到的地址")

    send_parsers.set_defaults(func=send_cmd)

    args = parser.parse_args(params)
    args.func(args)


def main(argv=sys.argv[1:]):
    """服务启动入口.

    设置覆盖顺序`环境变量>命令行参数`>`'-c'指定的配置文件`>`项目启动位置的配置文件`>默认配置.
    """
    parser_args(argv)
