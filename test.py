from tradingview_ta import TA_Handler, Interval

import time
from datetime import datetime
import datetime
from firebase import* 
import json
import requests


a=5
    # INTERVAL_1_MINUTE = "1m"
    # INTERVAL_5_MINUTES = "5m"
    # INTERVAL_15_MINUTES = "15m"
    # INTERVAL_30_MINUTES = "30m"
    # INTERVAL_1_HOUR = "1h"
    # INTERVAL_2_HOURS = "2h"
    # INTERVAL_4_HOURS = "4h"
    # INTERVAL_1_DAY = "1d"
    # INTERVAL_1_WEEK = "1W"
    # INTERVAL_1_MONTH = "1M"


def get_data(key, j):
            url = key+symbols[j]  
            data = requests.get(url)
            data = data.json()
            return data
def get_price_data(price_data,volatility_data):
        price=float(price_data['price'])
        price_change_percent=volatility_data['priceChangePercent']
        high_price=float(volatility_data['highPrice'])
        low_price=float(volatility_data['lowPrice'])
        high_curr=float(volatility_data['highPrice'])-(float(price_data['price']))
        low_curr=float(volatility_data['lowPrice'])-(float(price_data['price']))
        return price, price_change_percent, high_price, low_price, high_curr, low_curr   
def get_recommend(timer):
    output= TA_Handler(
            symbol=symbol,
            screener='Crypto',
            exchange='Binance',
            interval=timer
        )
    recommend=output.get_analysis().summary["RECOMMENDATION"]
    return recommend

 

  
while(True):
    symbols=['ETHUSDT', 'BNBUSDT', 'LTCUSDT', 'BTCUSDT','XRPUSDT','DOGEUSDT','LINKUSDT']
    key = "https://api.binance.com/api/v3/ticker/price?symbol="
    key2 = "https://api.binance.com/api/v3/ticker/24hr?symbol="
    date=datetime.datetime.now()
    dt_string = date.strftime("%d-%m-%Y %H:%M")

    j = 0
    for symbol in symbols:
            price_data=get_data(key, j)
            volatility_data=get_data(key2, j)
            price, price_change_percent, high_price, low_price, high_curr, low_curr=get_price_data(price_data,volatility_data)
            time_frame=['15m', '1h', '4h', '1d']
            for timer in time_frame:

                recommend=get_recommend(timer)
                result={'symbol':f'{symbol}', 'data':f'{dt_string}', 
                        'recomendation':f'{recommend}', 'price':f'{price}$',
                        'price change percent':f'{price_change_percent}%', 'high price': f'{high_price}$',
                        'low price':f'{low_price}$', 'high&curr':f'{high_curr}$', 'low&curr':f'{low_curr}$'}
                # print(result)
                #upload to the database
                database.child(f'Curr_{timer}').child(f'{dt_string}').child(f'Coin_{symbol}').set(result)
                print(result)
            j+=1
        
        

    time.sleep(300)
    print('-----------------------------------')



