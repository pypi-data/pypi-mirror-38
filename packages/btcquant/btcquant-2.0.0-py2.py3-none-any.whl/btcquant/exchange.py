#!/usr/bin/python
# -*- coding: utf-8 -*-
# 统一交易所接口
import json
import urllib.request, urllib.parse
import time, datetime
import hashlib, hmac
import numpy as np
import sys,os
from btcquant.config import exchanges

class EXCHANGES:

    def __init__(self, exchange = "gateio", apikey = "", secret = ""):
        if exchange not in exchanges:
            print('不存在的交易所 %s'%(exchange))

        self.__exchange = exchange
        self.__config = exchanges[exchange]
        self.__apikey = apikey
        self.__secret = secret
        print('Exchange: %s'%(self.__exchange))

    # 转换为交易所货币对格式，
    # 标准格式 BTC_USDT，转为各交易所的格式
    def _x_symbol(self, symbol):
        symbol_list = symbol.split("_")
        if self.__exchange == "gateio":     #btc_usdt
            new_symbol = symbol_list[0].lower() + "_" + symbol_list[1].lower()
        else:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))

        return new_symbol


    # 货币对列表 。返回列表，其中各项为字典
    def markets(self):
        url = self.__config["api"]["markets"]
        # print(url)
        markets = self.http_request(url)

        pairs = []
        if self.__exchange == "gateio":
            for item in markets:
                coincoin = item.split("_")
                pairs.append(item)
        else:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))

        return markets


    # 获取行情，返回字典 {"bid":7425.8723,"ask":7448.1439,"last":7448.1439}
    def ticker(self, symbol = 'BTC_USDT'):
        new_symbol = self._x_symbol(symbol)
        url = (self.__config["api"]["ticker"] % (new_symbol))
        # print(url)
        result = self.http_request(url)

        dict = {}
        if self.__exchange == "gateio":    
            dict = {'bid': result["highestBid"], 'ask': result["lowestAsk"], 'last': result["last"]}
        else:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))

        return dict


    # 获取市场深度，格式 {"asks":[[7615,0.04391],[7612.088,0.137511]],"bids":[[7480.2066,1],[7479.2113,0.3]]}
    def depth(self, symbol = 'BTC_USDT', limit = 100):
        new_symbol = self._x_symbol(symbol)
        new_limit = "step0" if self.__exchange == "huobi" else limit
        if not self.__config["api"]["depth"]:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))
            return None

        if self.__exchange == "gateio":
            url = (self.__config["api"]["depth"] % (new_symbol))
        else:
            url = (self.__config["api"]["depth"] % (new_symbol, new_limit))
        # print(url)
        result = self.http_request(url)
        # print(result)

        dict = {}
        if self.__exchange == "gateio":
            bids, asks = [], []
            for i in range(len(result["bids"])):
                bids.append(list(map(float, [result["bids"][i][0], result["bids"][i][1]])))
                asks.insert(0, list(map(float, [result["asks"][i][0], result["asks"][i][1]])))
            dict = {'asks': asks, 'bids': bids}
        else:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))

        return dict

    # 获取的K线数据，转换成矩阵
    def kline(self, symbol = 'BTC_USDT', interval = '1hour', limit = 120, latest = True):
        time.sleep(1)
        new_symbol = self._x_symbol(symbol)

        if not self.__config["api"]["kline"]:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))
            return None

        if not self.__config["period"][interval]:
            print('ERROR %s for %s NOT IN %s'%(self.__exchange, interval, sys._getframe().f_code.co_name))
            return None

        new_interval = self.__config["period"][interval]

        if self.__exchange == "gateio":
            url = (self.__config["api"]["kline"] % (new_symbol, new_interval, limit * int(int(new_interval) / 3600)))

        # print(url)
        result = self.http_request(url)
        # print(result)

        if self.__exchange == "gateio":
            npa = np.array(result["data"], dtype='float64')
            stamp, open, high, low, close, volume  = npa.T[0] / 1000,    npa.T[5],    npa.T[3],    npa.T[4],    npa.T[2],    npa.T[1]
        else:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))
            return None

        if not latest: #当前时间段没有走完，丢弃
            stamp, open, high, low, close, volume = stamp[:-1], open[:-1], high[:-1], low[:-1], close[:-1], volume[:-1]

        debug = False
        debug = True
        if debug:
            for x in range(0, 2, 1):
                time_local = time.localtime(stamp[x])
                dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                print("%s \t开：%.8f \t高：%.8f \t低：%.8f \t收：%.8f \t量：%.8f" % (dt, open[x], high[x], low[x], close[x], volume[x]))
            print("- " * 6)
            for x in range(-3, 0, 1):
                time_local = time.localtime(stamp[x])   #毫秒级时间戳转日期时间 相差8小时
                dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                print("%s \t开：%.8f \t高：%.8f \t低：%.8f \t收：%.8f \t量：%.8f" % (dt, open[x], high[x], low[x], close[x], volume[x]))
            print()
        return stamp, open, high, low, close, volume

    # http请求
    def http_request(self, url, method = "GET", params = None):
        try:
            req = urllib.request.Request(url)
            # req.add_header('X-MBX-APIKEY', self.__apikey)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0')

            if method == "GET":
                f = urllib.request.urlopen(req)
            elif method == "POST": # POST
                data = urllib.parse.urlencode(params).encode('utf-8')
                f = urllib.request.urlopen(req, data)
            elif method == "DELETE":
                req.method = lambda:'DELETE'
                f = urllib.request.urlopen(req, data)

            return json.loads(f.read().decode('utf-8'))
        except Exception as e:
            print(repr(e))
            print(url)
            print(params)
            time.sleep(1)


if __name__ == '__main__':

    fruit_list = ['gateio']
    for fruit in fruit_list:
        # os.system("clear")
        client = EXCHANGES(fruit)
        markets = client.markets()
        print(markets)

        ticker = client.ticker()
        print(ticker)

        depth = client.depth()
        print(depth)

        kline = client.kline(interval = '1hour')
        # print(kline)
        print("------------------from " + fruit)
        print()
        time.sleep(1)

