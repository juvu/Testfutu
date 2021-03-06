 #to find out what stock is uptrending
import pandas as pd
import pandas_ta as ta
import numpy as np
from futu import *
import talib
from talib import abstract
import numpy as np

def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

#create empty dataframe
column_names = ["Stock"]
df = pd.DataFrame(columns = column_names)

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111) #make connection

#set today
def DayStr(Tday): #function to return date in specific format
  Tday = Tday.strftime("%Y-%m-%d")
  return Tday

today = datetime.today()
#today = today.strftime("%Y-%m-%d")
NumDay = 30 #set the number of day of data



for code in range(1,9999,1):
  print('stock' + str(code))
  while len(str(code)) <= 4:#stock code to sting
    code = '0' + str(code)
  #get history data  
  ret, data, page_req_key = quote_ctx.request_history_kline('HK.' + code, start=DayStr(today - timedelta(days=NumDay)), end='', max_count=100, fields=KL_FIELD.ALL, ktype=KLType.K_DAY) 
  if ret == RET_OK:
    print('data ok')
  else:
    print('error:', data)
    continue
  #get snap data
  ret, snapdata = quote_ctx.get_market_snapshot(['HK.' + code])
  if ret == RET_OK:
    print('snap ok')
  else:
    print('error:', data)
    continue
    
  #check lot size and price per lot
  #print('lot_size')
  #print(snapdata.iloc[0].lot_size * snapdata.iloc[0].last_price)
  if snapdata.iloc[0].lot_size * snapdata.iloc[0].last_price > 10000:
    continue
  
  #calculate bias

  if len(data) == 0:
     continue
  MA = abstract.MA(data.close, timeperiod=12, matype=0)
  print('MA:' + str(MA))
  bias = (data.iloc[-1].close - MA[len(MA)-1])/(MA[len(MA)-1])
  if bias < 0:
    df = df.append({'Stock number':code}, ignore_index=True)  
  sleep(15)
quote_ctx.close() #close connection
df.to_csv('filter.csv', encoding='utf-8', index=False)
