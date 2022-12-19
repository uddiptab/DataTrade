import pandas as pd 
import numpy as np
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime
import time
import entry as et 
#######################################
# Initialization
######################################
client_id="H8O8SRR6U6-100"
# reading access token
f=open('../Input/token.txt','r')
for line in f:
	access_token=line 
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,log_path="../Log/")
print(" Intialized the app.... Access token read")


data = {
      "symbol":"NSE:HINDALCO-EQ",
      "qty":1,
      "type":2,
      "side":-1,
      "productType":"BO",
      "limitPrice":0,
      "stopPrice":0,
      "validity":"DAY",
      "disclosedQty":0,
      "offlineOrder":"False",
      "stopLoss":3,
      "takeProfit":3
    }

#print(fyers.place_order(data))
print(fyers.positions())
#print(fyers.orderbook())

