import pandas as pd 
import numpy as np
from kiteconnect import KiteConnect
import datetime
import time 
import logging
import math
import calendar
from os.path import exists 

####################################
# Declare the variables
####################################
API_KEY="cvnpw76nrxxgskao"
SECRET_KEY="vqvr1bv3ya07zctndtgq7v71c8vxu33t"
ACCESS_TOKEN="xYqtxU8cAP4IpRoKqJ39cURhfcnTEqJz"
kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)




###################################
# Log File Create
##################################
def write_log(text):
	'''
	Logging for 30 min positions
	'''
	today = datetime.date.today()
	date=today.strftime("%Y-%m-%d")
	file=open('../Log/'+date+'Zerodhafut_entry.txt','a')
	text1=("{}: ".format(datetime.datetime.now()))
	file.write(text1+" "+text+"\n")
	file.close()

###################################
# Option strike price calculation
###################################
def find_nearest_call_strike(ltp):
	'''
	Finds the nearest call price to hedge the short future
	'''
	ltp = math.ceil(ltp)
	ltp = int(ltp/100)
	new_ltp=100*(ltp+1)
	if (new_ltp-ltp)<50:
		new_ltp=new_ltp+50
	return new_ltp

def find_nearest_call_instrument(symbol,strike,month):
	'''
	Finds the option instrument
	symbol: 'NSE:NIFTY 50' or something like this
	strike: 18300 or something like this
	month:DEC or something like this
	returns NIFTYDEC18300CE
	'''
	if '50' in symbol:
		ins='NIFTY'+month+str(strike)+'CE'
	if 'BANK' in symbol:
		ins='BANKNIFTY'+month+str(strike)+'CE'
	return ins

def get_current_month():
	month=datetime.datetime.now().month
	month_string=calendar.month_name[month]
	mstr=month_string.upper()
	return mstr[0:3]



###################################
# Check the data first red candle 
###################################
ltp_collect_list=['NSE:NIFTY 50']

FIRST_RED_CANDLE_SEEN_NIFTY = False
FIRST_RED_CANDLE_SEEN_BNF = False


prev_ltp={}
for symbol in ltp_collect_list:
	prev_ltp[symbol]=None

####################################
# Check entry criteria
####################################

ORDER_DETAILS_FILE_PATH="../Input/order_details.csv"
def create_order_details(ORDER_DETAILS_FILE_PATH):
	'''
	Creates the csv file if not already created
	'''
	if not exists(ORDER_DETAILS_FILE_PATH):
		#Create the csv file
		df=pd.DataFrame(columns=['SYMBOL','FUT_ENTRY_TYPE','FUT_SYMBOL','OPT_SYMBOL','FUT_BUY_PRICE','FUT_SELL_PRICE','FUT_SL','FUT_TP','FUT_ORDER_ID','OPT_ORDER_ID','FUT_POS_STATUS','OPT_POS_STATUS'])
		df.to_csv(ORDER_DETAILS_FILE_PATH,index=False)
		print(" Order details files created...")


def get_sl_tp(symbol,position_type,high,low,ltp):
	sl=0
	tp=0
	quantity=0
	#Check ig the symbol is NIFTY or BANK NIFTY
	if 'BANK' in symbol:
		quantity=25
	else:
		diff= abs(high-low)
		if diff>60:
			diff=60
			quantity=50
	if position_type=='SELL':
		sl=low+diff
		target=low-(2*diff)
		target=math.ceil(target)
	return quantity,sl,tp




def check_entry(symbol,high,low,ltp,prev_ltp):
	'''
	high/loq: High and Low of first red candle
	ltp/prev_ltp: Current ltp and previous ltp
	'''
	if prev_ltp>=low and prev_ltp<=high:
		if ltp<low:
			print(" Sell signal generated in {}".format(symbol))
			quantiy,sl,tp=get_sl_tp(symbol,'SELL',high,low,ltp)

		else:
			print(" Checking.....{}".format(datetime.datetime.now()))

def position_taken(symbol):
	pass

def write_to_csv_fut(symbol,fut_order_id,opt_order_id,status):
	pass

def exit_orders_and_modify_csv(symbol,fut_order_id,opt_order_id,status):
	pass



###########################################
# Final Loop
###########################################
try:
	create_order_details(ORDER_DETAILS_FILE_PATH)
	write_log("INFO:\tOrder details file created")
except Exception as e:
	write_log("ERROR:\t Error in order details file creation")
	write_log(e)


while True:

	#Check if first red candle is seen yet
	if not FIRST_RED_CANDLE_SEEN_NIFTY:
		high=0
		low=0
		try:
			df = pd.read_csv('../Data/Intraday/5min/NIFTY50.csv',header= 0 )
			opens=df['O'].values
			closes=df['C'].values
			highs=df['H'].values
			lows=df['L'].values
			for i in range(0,len(df)):
				if closes[i]<opens[i]:
					if abs(highs[i]-lows[i])<70:
						FIRST_RED_CANDLE_SEEN_NIFTY=True
						high=highs[i]
						low=lows[i]
			
		except Exception as e:
			print(" ERROR: No data file")
			print(e)
	print(" NIFTY High: {} Low: {} ".format(high,low))
	try:
		quote=kite.ltp(ltp_collect_list)
		print(quote)
		for scrips in ltp_collect_list:
			ltp=quote[scrips]['last_price']
			print("{} ltp: {} prev_ltp:{}".format(scrips,ltp,prev_ltp[scrips]))

			# get the current month string
			currr_month = get_current_month()

			#Get the strike price
			strike = find_nearest_call_strike(ltp)

			#Get the option instrument
			opt_inst=find_nearest_call_instrument(symbol,strike,currr_month)

			print(" The nearest call option instrument : {}".format(opt_inst))



			prev_ltp[scrips]=ltp #reassign the ltp to prev_ltp


			

	except Exception as e:
		print(e)




	time.sleep(5)
