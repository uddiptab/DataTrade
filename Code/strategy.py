import pandas as pd 
import numpy as np
import datetime
import time













########################################
#1.  BNF First 5 min Red candle
########################################
def fetch_triggers_bnf_first_red():
	'''
	Fetch the High Low of first 5 min red candle
	'''
	df=pd.read_csv('../Data/Intraday/5min/BNF.csv',header=0)
	high=df['H'].values[-1]
	low=df['L'].values[-1]
	# Reading data for bankbees
	df=pd.read_csv('../Data/Intraday/5min/BANKBEES.csv',header=0)
	high=df['H'].values[-1]
	low=df['L'].values[-1]
	return high,low,bees_high,bees_low

def determines_sl_tp_bnf_first_red(trade_type,high,low,bees_high,bees_low):
	'''
	Dtermines the SL,TP for the trade
	'''
	buffer=0
	high=high+buffer
	low=low-buffer
	diff=abs(high-low)
	quantity=math.ceil(MAX_BEES_LOSS_PER_TRADE/abs(bees_high-bees_low))		# Quantity calculated on Bees
	qt1=math.ceil(quantity*0.7) #70% quantity which will be exited at tp1
	qt2=quantity-qt1 #Remaining quantity will be exited in tp 2
	# Only SELL
	if trade_type=='SELL':
		sl=high
		if diff>2:
			sl=low+2
		tp1=low-(2*diff)
		tp2=low-(3*diff)

	return int(quantity),int(qt1),int(qt2),sl,tp1,tp2


def BNF_first_red(symbol,ltp,prev_ltp):
	'''
	main strategy function for first red candle
	'''
	#basic variables which will be returned
	flag=False
	trade_type='NA'
	strategy='NA'
	quantity=0
	sl=0
	qt1=0 
	qt2=0 
	tp1=0 
	tp2=0  
	candle_high,candle_low,bees_high,bees_low=fetch_triggers_bnf_first_red()
	
	# Sell condition
	if prev_ltp>=candle_low and prev_ltp<candle_high and ltp<candle_low:
		flag=True
		trade_type='SELL'
		strategy='BNF_first_red'
		quantity,qt1,qt2,sl,tp1,tp2=determines_sl_tp_bnf_first_red(trade_type,candle_high,candle_low,bees_high,bees_low)

	return flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2



################################################
# NIFTY 12:45 candle module
################################################
def fetch_triggers_nifty1245():
	'''
	Fetch the High Low of first 5 min red candle
	'''
	df=pd.read_csv('../Data/Intraday/5min/NIFTY1245.csv',header=0)
	high=df['H'].values[-1]
	low=df['L'].values[-1]
	# Reading data for bankbees
	df=pd.read_csv('../Data/Intraday/5min/NIFTYBEES1245-EQ.csv.csv',header=0)
	high=df['H'].values[-1]
	low=df['L'].values[-1]
	return high,low,bees_high,bees_low


def determines_sl_tp_nifty1245(trade_type,high,low,bees_high,bees_low):
	'''
	Dtermines the SL,TP for the trade
	'''
	buffer=0
	high=high+buffer
	low=low-buffer
	diff=abs(high-low)
	quantity=math.ceil(MAX_BEES_LOSS_PER_TRADE/abs(bees_high-bees_low))		# Quantity calculated on Bees
	qt1=math.ceil(quantity*0.7) #70% quantity which will be exited at tp1
	qt2=quantity-qt1 #Remaining quantity will be exited in tp 2

	if trade_type=='BUY':
		sl=low
		# if sl is too high i.e. >40 for nifty then sl=high-40
		if diff > 0.6 :
			sl=high-0.6

		tp1= high+(2*diff)
		tp2=high+(3*diff)

	if trade_type=='SELL':
		sl=high
		if diff>0.6:
			sl=low+0.6
		tp1=low-(2*diff)
		tp2=low-(3*diff)

	return int(quantity),int(qt1),int(qt2),sl,tp1,tp2

def nifty_1245_strategy(symbol,ltp,prev_ltp):
	'''
	main strategy function for first red candle
	'''
	#basic variables which will be returned
	flag=False
	trade_type='NA'
	strategy='NA'
	quantity=0
	sl=0
	qt1=0 
	qt2=0 
	tp1=0 
	tp2=0  
	try:
		candle_high,candle_low,bees_high,bees_low=fetch_triggers_nifty1245()
		
		# Check for BUY Condition
		if prev_ltp<=candle_high and prev_ltp>candle_low and ltp>candle_high:
			flag=True
			trade_type='BUY'
			strategy='NIFTY1245'
			quantity,qt1,qt2,sl,tp1,tp2=determines_sl_tp_nifty1245(trade_type,candle_high,candle_low,bees_high,bees_low)

		# Sell condition
		if prev_ltp>=candle_low and prev_ltp<candle_high and ltp<candle_low:
			flag=True
			trade_type='SELL'
			strategy='NIFTY1245'
			quantity,qt1,qt2,sl,tp1,tp2=ddetermines_sl_tp_nifty1245(trade_type,candle_high,candle_low,bees_high,bees_low)
	except Exception as e:
		print(e)

	return flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2



##################################################
# NIFTY 5 EMA STRATEGY
##################################################



#################################################
# JPYINR Second Hour strategy
#################################################
def fetch_triggers_jpy():
	'''
	Fetches second 1 hour candle High low
	'''
	df=pd.read_csv('../Data/Intraday/1hour/JPYINR.csv',header=0)
	if len(df)>1:
		high=df['H'].values[1]
		low=df['L'].values[1]
	else:
		high=0
		low=0
	return high,low




#################################################
# First red Candle Short
################################################
def fetch_triggers_first_red_short(filename):
	# fetch the High Low of the first red candle for the particular stock
	df = pd.read_csv('../Data/Intraday/5min/'+filename+'.csv',header = 0)
	if len(df)>0:
		highs=df['H'].values
		lows=df['L'].values
		for i in range(0,len(df)):
			if highs[i]<lows[i]:
				high = highs[i]
				low = =lows[i]
				break
			else:
				high = 0
				low = 0
	else:
		high=0
		low=0
	return high,low


def determine_sl_tp_first_red_short(trade_type,high,low):
	MAX_LOSS_PER_TRADE = 200
	buffer=0
	high=high+buffer
	low=low-buffer
	diff=abs(high-low)
	# Check if the difference is more than 0.7% of the stock price
	if diff > 0.007*high:
		diff = 0.007*high
		diff = round(diff,2)
	quantity=math.ceil(MAX_LOSS_PER_TRADE/diff)		# Quantity calculated on Bees
	qt1=math.ceil(quantity*0.7) #70% quantity which will be exited at tp1
	qt2=quantity-qt1 #Remaining quantity will be exited in tp 2
	# Only SELL
	if trade_type=='SELL':
		sl=high
		tp1=low-(2*diff)
		tp2=low-(3*diff)
	tp1=round(tp1,2)
	tp2=round(tp2,2)


	return int(quantity),int(qt1),int(qt2),sl,tp1,tp2

def first_red_candle_short(symbol,ltp,prev_ltp):
	
	#basic variables which will be returned
	flag=False
	trade_type='NA'
	strategy='NA'
	quantity=0
	sl=0
	qt1=0 
	qt2=0 
	tp1=0 
	tp2=0  

	try:
		filename = stock
		high,low = fetch_triggers_first_red_short(filename)
		print(" For {} First Red Candle High:{} and Low:{}".format(high,low))

		#Strategy
		if prev_ltp>=low and ltp<low:
			flag=True
			trade_type='SELL'
			Strategy='First red Short'
			quantity,qt1,qt2,sl,tp1,tp2 = determine_sl_tp_first_red_short(trade_type,high,low)

	return flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2




##############################################
# First 5 min Candle BO (only 3 stock)
##############################################
def fetch_triggers_first_5min_bo(filename):
	df = pd.read_csv('../Data/Intraday/5min'+filename+'.csv',header=0)
	if len(df)>0:
		high=df['H'].values[0]
		low=df['L'].values[0]
	else:
		high = 0
		low = 0
	return high,low

def determine_sl_tp_first_5min_bo(trade_type,high,low):
	MAX_LOSS_PER_TRADE = 200
	buffer=0
	high=high+buffer
	low=low-buffer
	diff=abs(high-low)
	# Check if the difference is more than 0.7% of the stock price
	if diff > 0.007*high:
		diff = 0.007*high
		diff = round(diff,2)
	quantity=math.ceil(MAX_LOSS_PER_TRADE/diff)		# Quantity calculated on Bees
	qt1=math.ceil(quantity*0.7) #70% quantity which will be exited at tp1
	qt2=quantity-qt1 #Remaining quantity will be exited in tp 2
	#Signal is BUY
	if trade_type=='BUY':
		sl = low
		tp1=high+(2.2*diff)
		tp2 = high+(3*diff)


	# Only SELL
	if trade_type=='SELL':
		sl=high
		tp1=low-(2.2*diff)
		tp2=low-(3*diff)

	tp1 = round(tp1,2)
	tp2=round(tp2,2)

	return int(quantity), int(qt1),int(qt2),sl,tp1,tp2


def first_5min_bo(symbol,ltp,prev_ltp):
	flag=False
	trade_type='NA'
	strategy='NA'
	quantity=0
	sl=0
	qt1=0 
	qt2=0 
	tp1=0 
	tp2=0

	try:
		filename = stock
		high,low = fetch_triggers_first_5min_bo(filename)
		print(" For {} First 5min High:{} and Low:{}".format(high,low))

		#Strategy
		if prev_ltp<=high and ltp>high:
			flag=True
			trade_type='BUY'
			Strategy='First 5 min BO'
			quantity,qt1,qt2,sl,tp1,tp2 = determine_sl_tp_first_5min_bo(trade_type,high,low)


		if prev_ltp>=low and ltp<low:
			flag=True
			trade_type='SELL'
			Strategy='First 5 min BO'
			quantity,qt1,qt2,sl,tp1,tp2 = determine_sl_tp_first_5min_bo(trade_type,high,low)

	return flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2

	


















