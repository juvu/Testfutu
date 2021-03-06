#-*- coding: utf-8 -*
from datetime import datetime
import pandas as pd
import pandas_ta as ta
import numpy as np
import matplotlib.pylab as plt
from futu import *
import talib
from talib import abstract
import numpy as np
import random
import argparse
import pdb
import os

'''
while True:
  now = datetime.now()
  print(now)
  print(now.minute)
  if now.minute%3 == 0:
     print('!!!!!!wokr')
  time.sleep(10)
'''  
code = '58558'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
ret, order = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
temp = order.loc[(order['code'] == 'HK.' + str(code)) & (order['trd_side'] == 'SELL')].create_time.max()
print(order)
print('~~')
print(temp)
print('~~')
print(order.loc[order['create_time'] == temp].order_status)
print('~~')
print(order.loc[order['create_time'] == temp].order_status.max())
print('~~')
if (order.loc[order['create_time'] == temp].order_status.max()) == 'FILLED_ALL':
  print('ok')
time.sleep(100)
  
now = datetime.now()
today930 = now.replace(hour=9, minute=35, second=0, microsecond=0)
today11 = now.replace(hour=11, minute=0, second=0, microsecond=0)
today13 = now.replace(hour=13, minute=0, second=0, microsecond=0)
today15 = now.replace(hour=15, minute=0, second=0, microsecond=0)

print(today930)
print(today11)
print(today13)
print(today15)

if (now > today930 and now < today11) or (now > today13 and now < today15):
  print('trade')
else:
  print('no trade')

NumPos = 0  
count = 0
size = 50
code = '00981'
pwd_unlock = '878900'
trd_ctx = OpenHKTradeContext(host='127.0.0.1', port=11111)
quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
ret_sub, err_message = quote_ctx.subscribe(['HK.' + code], [SubType.K_1M], subscribe_push=False)

#subscribtion
if ret_sub == RET_OK:  # 订阅成功
    print('ok')
else:
    print('subscription failed', err_message)
ret, data = quote_ctx.get_cur_kline('HK.' + code, 30, SubType.K_1M, AuType.QFQ)  
if ret == RET_OK:
  print(data[-3:])
else:
  print('error:', data) 
        
#unlock
print(trd_ctx.unlock_trade(pwd_unlock))
ret, data = quote_ctx.get_cur_kline('HK.' + code, 30, SubType.K_1M, AuType.QFQ)
ret_code, info_data = trd_ctx.accinfo_query(trd_env = TrdEnv.SIMULATE)   #get ac info
ret, snapdata =quote_ctx.get_market_snapshot(['HK.' + code])
size = snapdata.iloc[-1].lot_size
print('~~~~~~')

print(info_data.iloc[-1].cash)
print(data.iloc[-1].close)
print(data.iloc[-1].close*size)
print('~~~~~~')

if info_data.iloc[-1].cash > ((data.iloc[-1].close)*(size)):
  print('debugged1')
if info_data.iloc[-1].cash <= ((data.iloc[-1].close)*(size)):
  print('debugged2')
'''    
ret,orderinfo = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
print(orderinfo)
print(len(orderinfo))
if len(orderinfo) > 0: 
  datetime_object = datetime.strptime(orderinfo.iloc[-1].updated_time , '%Y-%m-%d %H:%M:%S')
  diff = datetime_object - datetime.now()
'''    
#place order
'''
print(trd_ctx.place_order(price = data.iloc[-1].close, order_type = OrderType.NORMAL, qty=size*10, code='HK.' + code, trd_side=TrdSide.BUY,trd_env=TrdEnv.SIMULATE))
    
    #check successful trade
while True:
  time.sleep(5)
  ret, query = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
  if query.iloc[-1].order_status == 'FILLED_ALL':
    NumPos = NumPos + size
    break
  elif count < 2:
    count +=1
    print(count)
  else:
    print('cancel order')
    trd_ctx.cancel_all_order(trd_env = TrdEnv.SIMULATE)
'''
'''
ret,orderlist = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE)
if ret == RET_OK:
  print('order list ok')
else:
  print('fail')
  print(orderlist.order_id)
print('pt1')
for i in range (0,len(orderlist)-1):
  print(i)
  print('pt2')
  print(orderlist.iloc[i].order_id)
  print(trd_ctx.modify_order(price = data.iloc[-1].close, qty = 500,modify_order_op = ModifyOrderOp.CANCEL, order_id = orderlist.iloc[i].order_id,trd_env = TrdEnv.SIMULATE))
count = 0
    #break
'''
'''
ret_code, info_data = trd_ctx.accinfo_query(trd_env = TrdEnv.SIMULATE)
print(info_data)
trd_ctx.place_order(price = data.iloc[-1].close,code = code, qty = NumPos,trd_side =TrdSide.SELL,order_type = OrderType.MARKET, trd_env = TrdEnv.SIMULATE)

postlist = trd_ctx.position_list_query(trd_env = TrdEnv.SIMULATE)
orderlist = trd_ctx.order_list_query(trd_env = TrdEnv.SIMULATE,status_filter_list=OrderStatus.SUBMITTED)
for i in range (-1,-len(orderlist)+1):
  trd_ctx.modify_order(ModifyOrderOp.CANCEL, order_id = orderlist[i].order_id,trd_env = TrdEnv.SIMULATE)
#print(trd_ctx.cancel_all_order(trd_env = TrdEnv.SIMULATE))
for i in range (-1,-len(postlist)+1):
  print('loop')
  print(i)
  trd_ctx.place_order(code = postlist[i].code, qty = postlist[i].qty,trd_side =TrdSide.SELL,OrderType = 'MARKET', trd_env = TrdEnv.SIMULATE)
'''
trd_ctx.close()  
quote_ctx.close()
