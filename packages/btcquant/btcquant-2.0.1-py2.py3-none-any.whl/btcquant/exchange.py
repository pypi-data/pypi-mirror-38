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


    # 标准格式 BTC_USDT，转为各交易所的格式
    def _x_symbol(self, symbol):
        symbol_list = symbol.split("_")
        if self.__exchange == "binance":    #BTCUSDT
            new_symbol = symbol_list[0] + symbol_list[1]
        elif self.__exchange == "huobi":    #btcusdt
            new_symbol = symbol_list[0].lower() + symbol_list[1].lower()
        elif self.__exchange == "okex" or self.__exchange == "zb" or self.__exchange == "gateio":     #btc_usdt
            new_symbol = symbol_list[0].lower() + "_" + symbol_list[1].lower()
        elif self.__exchange == "bitfinex": #tBTCUSD
            new_symbol = "t" + symbol_list[0] + symbol_list[1][0:3]
        elif self.__exchange == "bittrex":  #'USDT-BTC'
            new_symbol = symbol_list[1] + "-" + symbol_list[0]
        else:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))

        return new_symbol


    # 货币对列表 。返回列表，其中各项为字典
    def markets(self):
        url = self.__config["api"]["markets"]
        print(url)
        markets = self.http_request(url)

        pairs = []
        if self.__exchange == "binance":
            for item in markets["data"]:
                if item["status"] == "TRADING":
                    pairs.append({'symbol': item["symbol"], 'quote': item["quoteAsset"]})
        elif self.__exchange == "huobi":
            for item in markets["data"]:
                pairs.append({'symbol': item["symbol"], 'quote': item["quote-currency"].upper()})
        elif self.__exchange == "okex":
            for item in markets["data"]:
                if item["online"] == 1:
                    temp = item["symbol"].split("_")
                    pairs.append({'symbol': item["symbol"], 'quote': temp[1].upper()})
        elif self.__exchange == "bitfinex":
            for item in markets:
                quote = "USDT" if item[-3:] == "usd" else item[-3:].upper()
                pairs.append({'symbol': item.upper(), 'quote': quote})
        elif self.__exchange == "bittrex":
            for item in markets["result"]:
                pairs.append({'symbol': item["MarketName"], 'quote': item["BaseCurrency"]})
        elif self.__exchange == "zb":
            for item, detail in markets.items():
                qc = item.split("_")
                pairs.append({'symbol': item, 'quote': qc[1].upper()})
        elif self.__exchange == "gateio":
            for item in markets:
                coincoin = item.split("_")
                pairs.append({'symbol': item.lower(), 'base': coincoin[0].upper(), 'quote': coincoin[1].upper()})
        else:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))

        return pairs


    # 获取行情，返回字典 {"bid":7425.8723,"ask":7448.1439,"last":7448.1439}
    def ticker(self, symbol = 'BTC_USDT'):
        new_symbol = self._x_symbol(symbol)
        url = (self.__config["api"]["ticker"] % (new_symbol))
        print(url)
        result = self.http_request(url)
        # print(result)

        dict = {}
        if self.__exchange == "binance":
            dict = {'bid': float(result["bidPrice"]), 'ask': float(result["askPrice"]), 'last': float(result["lastPrice"])}
        elif self.__exchange == "huobi":
            dict = {'bid': result["tick"]["bid"][0], 'ask': result["tick"]["ask"][0], 'last': result["tick"]["close"]}
        elif self.__exchange == "okex" or self.__exchange == "zb":
            dict = {'bid': float(result["ticker"]["buy"]), 'ask': float(result["ticker"]["sell"]), 'last': float(result["ticker"]["last"])}
        elif self.__exchange == "bitfinex":
            dict = {'bid': result[0], 'ask': result[2], 'last': result[6]}
        elif self.__exchange == "bittrex":
            dict = {'bid': result["result"]["Bid"], 'ask': result["result"]["Ask"], 'last': result["result"]["Last"]}
        elif self.__exchange == "gateio":    
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
        print(url)
        result = self.http_request(url)
        # print(result)

        dict = {}
        if self.__exchange == "binance":#转换较麻烦
            bids, asks = [], []
            for i in range(len(result["bids"])):
                bids.append([float(result["bids"][i][0]), float(result["bids"][i][1])])
                asks.append([float(result["asks"][i][0]), float(result["asks"][i][1])])
            dict = {'asks': asks, 'bids': bids}
        elif self.__exchange == "huobi":
            dict = {'asks': result["tick"]["asks"], 'bids': result["tick"]["bids"]}
        elif self.__exchange == "okex":
            dict = result   #标准格式，不用转换
        elif self.__exchange == "zb":
            dict = {'asks': result["asks"], 'bids': result["asks"]}
        elif self.__exchange == "gateio":
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
        time.sleep(1)  # 有的交易所 K线接口每秒只能请求一次数据。
        new_symbol = self._x_symbol(symbol)

        if not self.__config["api"]["kline"]:
            print('ERROR %s NOT IN %s'%(self.__exchange, sys._getframe().f_code.co_name))
            return None

        if not self.__config["period"][interval]:
            print('ERROR %s for %s NOT IN %s'%(self.__exchange, interval, sys._getframe().f_code.co_name))
            return None

        new_interval = self.__config["period"][interval]

        if self.__exchange == "bitfinex":
            url = (self.__config["api"]["kline"] % (new_interval, new_symbol, limit))
        elif self.__exchange == "gateio":
            url = (self.__config["api"]["kline"] % (new_symbol, new_interval, limit * int(int(new_interval) / 3600)))
        else:
            url = (self.__config["api"]["kline"] % (new_symbol, new_interval, limit))
        print(url)
        result = self.http_request(url)
        # print(result)

        #kline转矩阵，统一格式
        if self.__exchange == "binance" or self.__exchange == "okex":
            npa = np.array(result, dtype='float64')
            stamp, open, high, low, close, volume  = npa.T[0] / 1000,    npa.T[1],    npa.T[2],    npa.T[3],    npa.T[4],    npa.T[5]
        elif self.__exchange == "huobi":
            stamp, open, high, low, close, volume = [], [], [], [], [], []
            for index in range(len(result["data"]) - 1, -1, -1):
                stamp.append(float(result["data"][index]['id']))
                open.append(float(result["data"][index]['open']))
                high.append(float(result["data"][index]['high']))
                low.append(float(result["data"][index]['low']))
                close.append(float(result["data"][index]['close']))
                volume.append(float(result["data"][index]['amount']))
        elif self.__exchange == "bitfinex":
            npa = np.array(result)
            npa = npa[np.lexsort(npa[:,::-1].T)]    #按第一列顺序排序
            stamp, open, high, low, close, volume  = npa.T[0] / 1000,    npa.T[1],    npa.T[3],    npa.T[4],    npa.T[2],    npa.T[5]
        elif self.__exchange == "zb":
            npa = np.array(result["data"], dtype='float64')
            stamp, open, high, low, close, volume  = npa.T[0] / 1000,    npa.T[1],    npa.T[2],    npa.T[3],    npa.T[4],    npa.T[5]
        elif self.__exchange == "gateio":
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
        attempts = 0
        maxtimes = 3
        success = False
        while attempts < maxtimes and not success:
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

                success = True
                return json.loads(f.read().decode('utf-8'))
            except Exception as e:
                print(repr(e))
                print(url)
                print(params)
                time.sleep(1)
                attempts += 1
                if attempts == maxtimes:
                    return


if __name__ == '__main__':
    # # from api.binance.binanceapipy3 import EXCHANGES
    # # from indicator.TechAnalysis import TechAna


    # # os.system("cls")
    # # print (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))    #日期格式化

    # # #在 5分钟 和55分钟之间进行，防止数据时间戳不一致 取小时线时要注意
    # # if (int(datetime.datetime.now().strftime('%M')) <= 5):
        # # print("\033[7;37;40m数据可能未生成\t\033[0m")
        # # # exit()

    # # apikey = ''
    # # secret = ''

    # apikey = ""
    # secret = ""

    # os.system("clear")
    fruit_list = ['binance','huobi','okex','bitfinex']
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

