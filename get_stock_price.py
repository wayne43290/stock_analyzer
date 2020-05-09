# import package
from datetime import date,timedelta
from urllib.request import urlopen
from dateutil import rrule
import datetime
import pandas as pd
import numpy as np
import json
import time

stock_006208 = "006208"
stock_0050 = "0050"
stock_2884 = "2884"
stock_0056 = "0056"
stock_no = stock_0056     # TODO: adjust this
start_date = "2015-01-01"   # TODO: adjust this
end_date = "2020-05-01"     # TODO: adjust this

def craw_one_month(stock_number,date):
    url = (
        "http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date="+
        date.strftime('%Y%m%d')+"&stockNo="+stock_number
    )
    data = json.loads(urlopen(url).read())
    #print(data)
    # try to get 'date' and 'close price' only
    return pd.DataFrame(data['data']).iloc[:,[0,6]]
    #return pd.DataFrame(data['data'],columns=data['fields'])

# 根據使用者輸入的日期，以月為單位，重複呼叫爬取月股價的函式
def craw_stock(stock_number, start_month, end_month):
    b_month = date(*[int(x) for x in start_month.split('-')])
    e_month = date(*[int(x) for x in end_month.split('-')])
    
    result = pd.DataFrame()
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=b_month, until=e_month):
        result = pd.concat([result, craw_one_month(stock_number, dt)], ignore_index=True)
        time.sleep(2)
    
    return result

df = craw_stock(stock_no, start_date, end_date)
'''
df = df.drop(['成交金額'], axis=1)
df = df.drop(['成交股數'], axis=1)
df = df.drop(['開盤價'], axis=1)
df = df.drop(['最高價'], axis=1)
df = df.drop(['最低價'], axis=1)
df = df.drop(['漲跌價差'], axis=1)
df = df.drop(['成交筆數'], axis=1)
'''
df.to_csv('tsmc_' + stock_no + '.csv', sep='\t', header=False, index=False)