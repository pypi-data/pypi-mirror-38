# coding=utf-8

exes = {
                    "gateio":{
                        "period":{
                            "1min":"60",
                            "3min":"",
                            "5min":"300",
                            "10min":"600",
                            "15min":"900",
                            "30min":"1800",
                            "1hour":"3600",
                            "2hour":"7200",
                            "3hour":"10800",
                            "4hour":"14400",
                            "6hour":"21600",
                            "8hour":"28800",
                            "12hour":"43200",
                            "1day":"86400",
                            "3day":"259200",
                            "1week":"604800",
                            "2week":"",
                            "1month":""
                        },
                        "api":{
                            "markets":"https://data.gateio.io/api2/1/pairs",
                            "ticker":"https://data.gateio.io/api2/1/ticker/%s",
                            "depth":"https://data.gateio.io/api2/1/orderBook/%s",
                            "kline":"https://data.gateio.io/api2/1/candlestick2/%s?group_sec=%s&range_hour=%s"
                        }
                    }
                }
