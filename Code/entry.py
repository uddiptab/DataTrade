import pandas as pd 
import numpy as np
import strategy as st
import datetime
import time,math


###############################
# Handle Functions
###############################
def log_write_entry(text):
	'''
	Writes in the Log file
	'''
	today = datetime.date.today()
	date=today.strftime("%Y-%m-%d")
	file=open('../Log/'+date+'_entry.txt','a')
	text1=("{}: ".format(datetime.datetime.now()))
	file.write(text1+text+"\n")
	file.close()

def write_30min_log(text):
	'''
	Logging for 30 min positions
	'''
	today = datetime.date.today()
	date=today.strftime("%Y-%m-%d")
	file=open('../Log/'+date+'30min_entry.txt','a')
	text1=("{}: ".format(datetime.datetime.now()))
	file.write(text1+" "+text+"\n")
	file.close()




	

def place_bracket_order(symbol,trade_type,sl,tp,quantity,strategy):
	'''
	Place a BUY bracket order with params
	Write details with the name of the strategy in the transaction file
	'''
	if trade_type=='BUY':
		trade='1'
	if trade_type=='SELL':
		trade='-1'
	data = {
      "symbol":symbol,
      "qty":int(quantity),
      "type":2,
      "side":trade,
      "productType":"BO",
      "limitPrice":0,
      "stopPrice":0,
      "validity":"DAY",
      "disclosedQty":0,
      "offlineOrder":"False",
      "stopLoss":sl,
      "takeProfit":tp
    }
   
	fyers.place_order(data)
	print("Order placed")
    




def position_taken(symbol,strategy,entry_type,fyers):
	'''
	Checks if a particular position is already open
	1. Check if the SYMBOL is open in current positions
	2. Check from positions.csv
	3. Decide
	'''
	flag = False
	pos=fyers.positions()
	netPos=pos['netPositions']
	for trades in netPos:
		stock = trades['symbol']

		unrelProfit =trades['unrealized_profit']
		relProfit = trades['realized_profit']
		side = trades['side']

		if side==1:
			side = 'BUY'
		if side==-1:
			side = 'SELL'

		scrip=symbol
		print(scrip,stock,side,entry_type,relProfit)

		if (unrelProfit>0.0 or unrelProfit<0.0) and scrip== stock and side == entry_type:
			flag = True
			break
	return flag







#################################
# Entry criterions
#################################
def check_entry(symbol,ltp,prev_ltp,fyers):
	'''
	Checks for entry and places order if strategy is satisfied
	'''

	'''
	#1. For BankNifty trades
	if 'NIFTYBANK-INDEX' in symbol:
		flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2 = st.BNF_first_red(symbol,ltp,prev_ltp)
		if flag:
			print(" First red candle startegy hit at {}".format(datetime.datetime.now()))
			log_write_entry(" STRATEGYHIT: First red candle startegy hit")
			# Check if position is already not taken



	if 'NIFTY50-INDEX' in symbol:
		flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2 = st.nifty_1245_strategy(symbol,ltp,prev_ltp)
		if flag:
			print(" NIFTY 12:45 startegy hit at {}".format(datetime.datetime.now()))
			log_write_entry(" STRATEGYHIT: 12:45 candle startegy hit")

	'''

	# Check for First Red candle short stocks
	if 'NIFTY' not in symbol and 'JPY' not in symbol:

		# 1 . For First Red Candle short (5 min)

		first_red_short_stock_list_file = pd.read_csv('../Input/red_candle_short_stocks.csv',header=0)
		first_red_short_stock_list = first_red_short_stock_list_file['STOCKS'].values

		stock = symbol.split("-")[0]
		stock = stock[4:]
		print(" Checking details for:{} {}".format(symbol,stock))

		if stock in first_red_short_stock_list:
			flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2 = st.first_red_candle_short(stock,ltp,prev_ltp)

			# If the signal comes out as true
			if flag:
				print("{} Signal generated in {} at {}".format(trade_type,symbol,datetime.datetime.now()))
				write_30min_log("{} Signal generated in {} at {}".format(trade_type,symbol,datetime.datetime.now()))
				#Checks if position is not already taken in the same side
				if not position_taken(symbol,strategy,trade_type,fyers):	
					write_30min_log("-------------------------------------------------------------")
					write_30min_log(" Start SELL Position: First 5 min Red candle Short: {}".format(symbol))
					write_30min_log("-------------------------------------------------------------")
					if trade_type == 'SELL':
						print(" paramaters are trade_type:{} sl:{} qt1:{} qt2:{} Tp1:{} Tp2:{}".format(trade_type,sl,qt1,qt2,tp1,tp2))
						write_30min_log("INFO:\tPlacing SELL order First 5 min Red candle Short...")
						write_30min_log("INFO:\tparamaters are trade_type:{} sl:{} qt1:{} qt2:{} Tp1:{} Tp2:{}".format(trade_type,sl,qt1,qt2,tp1,tp2))
						try:
							response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp1,qt1,fyers)
							if response in None:
								print(" order placement error")
								write_30min_log("ERROR:\tOrder Placement error")
							else:
								print("*** order placed ***")
								write_30min_log("**** ORDER PLACED ****")

						except Exception as e:
							print(" ERROR: Order placement failed")
							print(e)
							write_30min_log("ERROR:\tOrder plaement failed in {}".format(symbol))
							write_30min_log(e)
						try:
							response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp2,qt2,fyers)
							if response is None:
								print(" order placement error")
								write_30min_log("ERROR:\tOrder Placement error")
							else:
								print("*** order placed ***")
								write_30min_log("**** ORDER PLACED ****")

						except Exception as e:
							print(" ERROR: Order placement failed")
							print(e)
							write_30min_log("ERROR:\t Order plaement failed in {}".format(symbol))
							write_30min_log(e)
					write_30min_log("------------------------------------------------------------\n")
						
						
				else:
					print(" Already in Position")
					write_30min_log("INFO:\tPosition already taken: In 5 min in {}".format(symbol))
				






######################################
# Function for 30 min BO STrategy
######################################
def fetch_available_reentry(stock):
	'''
	Function feteches how many re-entries are available for the particular stock
	from the ../Input/renetry.csv file
	'''
def calculate_buffer(ltp):
	buffer =1
	if ltp<200:
		buffer = 0.1
	if ltp>200 and ltp<500:
		buffer=0.2
	if ltp>500 and ltp<700:
		buffer = 0.5
	if ltp>700 and ltp<1500:
		buffer=1
	if ltp>1500 and ltp<3000:
		buffer =2
	if ltp>3000:
		buffer=4
	return buffer

def calculate_param(HIGH,LOW,ltp):
	MAX_RISK=500
	diff =abs(HIGH-LOW)
	if (ltp*0.5)/100 > diff:
		diff = round((ltp*0.5)/100,1)
	print("diff is:{}".format(diff))
	quantity = math.ceil(MAX_RISK/diff)
	qt1 = math.ceil(quantity*0.7)
	qt2=quantity-qt1
	tp1 = round(diff*2,1)
	tp2 = round(diff*3,1)
	return qt1,qt2,tp1,tp2




  
   
def place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp,quantity,fyers):
	'''
	Place a BUY bracket order with params
	Write details with the name of the strategy in the transaction file
	'''
	if trade_type=='BUY':
		trade='1'
	if trade_type=='SELL':
		trade='-1'
	data = {
      "symbol":symbol,
      "qty":int(quantity),
      "type":2,
      "side":trade,
      "productType":"BO",
      "limitPrice":0,
      "stopPrice":0,
      "validity":"DAY",
      "disclosedQty":0,
      "offlineOrder":"False",
      "stopLoss":sl,
      "takeProfit":tp
    }
   
	fyers.place_order(data)
	print("Order placed")



def check_30min_type1(symbol,ltp,prev_ltp,fyers):


	stock = symbol[4:-3] 
	flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2 = st.first_30min_bo_type1(stock,ltp,prev_ltp)
	print(type(sl),type(tp1))
	# If the signal comes out as true
	if flag:
		print("{} Signal generated in at {} 30 minTrade TYPE 1".format(trade_type,datetime.datetime.now()))
		write_30min_log("INFO:\t{} Signal generated in {} at {} 30  min Trade TYPE 1".format(trade_type,symbol,datetime.datetime.now()))
		#Checks if position is not already taken in the same side
		if not position_taken(symbol,strategy,trade_type,fyers):

			if trade_type == 'BUY':
				write_30min_log("--------------------------------------------------------")
				write_30min_log(" Start BUY Positions: 30 Min Trades (Type 1): {}".format(symbol))
				write_30min_log("--------------------------------------------------------")
				print(" Placing BUY order for 30 min BO Type 1...")
				print(" paramaters are trade_type:{} sl:{} qt1:{} qt2:{} Tp1:{} Tp2:{}".format(trade_type,sl,qt1,qt2,tp1,tp2))
				write_30min_log("INFO:\tPlacing BUY order for 30 min BO Type 1...")
				write_30min_log("INFO:\tparamaters are trade_type:{} sl:{} qt1:{} qt2:{} Tp1:{} Tp2:{}".format(trade_type,sl,qt1,qt2,tp1,tp2))
				try:
					response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp1,qt1,fyers)
					if response is None:
						print(" order placement error")
						write_30min_log("ERROR:\tOrder Placement error")
					else:
						print("*** prder placed ***")
						write_30min_log("**** ORDER PLACED ****")

				except Exception as e:
					print(" ERROR: Order placement failed")
					print(e)
					write_30min_log("ERROR:\tOrder plaement failed in {}".format(symbol))
					write_30min_log(e)

				try:
					response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp2,qt2,fyers)
					if response is None:
						print(" Order placement error")
						write_30min_log('ERROR:\t Order placement error')
					else:
						print(" ***Order placed***")
						write_30min_log("**** ORDER PLACED ****")

				except Exception as e:
					print(" ERROR: Order placement failed")
					print(e)
					write_30min_log("ERROR:\t Order plaement failed in {}".format(symbol))
					write_30min_log(e)
				write_30min_log("------------------------End of order --------------------------------\n")

			if trade_type == 'SELL':
				write_30min_log("--------------------------------------------------------")
				write_30min_log(" Start SELL Positions: 30 Min Trades (Type 1): {}".format(symbol))
				write_30min_log("--------------------------------------------------------")
				print(" Placing SELL order for 30 min BO Type 1...")
				print(" paramaters are trade_type:{} sl:{} qt1:{} qt2:{} Tp1:{} Tp2:{}".format(trade_type,sl,qt1,qt2,tp1,tp2))
				write_30min_log("INFO:\tPlacing SELL order for 30 min BO Type 1...")
				write_30min_log("INFO:\tparamaters are trade_type:{} sl:{} qt1:{} qt2:{} Tp1:{} Tp2:{}".format(trade_type,sl,qt1,qt2,tp1,tp2))
				try:
					response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp1,qt1,fyers)
					if response is None:
						print(" Order placement error")
						write_30min_log("ERROR:\tOrder placement error")
					else:
						print(" Order placed")
						write_30min_log("**** ORDER PLACED ****")
				except Exception as e:
					print(" ERROR: Order placement failed")
					print(e)
					write_30min_log("ERROR:\t Order plaement failed in {}".format(symbol))
					write_30min_log(e)
				try:
					response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp2,qt2,fyers)
					if response is None:
						print(" Order placement error")
						write_30min_log("ERROR:\tOrder palcement error")
					print(" Order placed")
					write_30min_log("**** ORDER PLACED ****")
				except Exception as e:
					print(" ERROR: Order placement failed")
					write_30min_log("ERROR:\t Order plaement failed in {}".format(symbol))
					write_30min_log(e)
				write_30min_log("-----------------------End of Order---------------------------------\n")
				
		else:
			print(" Already in Position")
			write_30min_log("INFO:\tPosition already taken: In 30 min loop")




###############################
# For Type 2
###############################
def check_30min_type2(symbol,ltp,prev_ltp,fyers):


	stock = symbol[4:-3] 
	flag,trade_type,strategy,quantity,sl,tp1 = st.first_30min_bo_type2(stock,ltp,prev_ltp)

	# If the signal comes out as true
	if flag:
		print("{} Signal generated in at {} Trade TYPE 2".format(trade_type,datetime.datetime.now()))
		write_30min_log("INFO:\t{} Signal generated in {} at {} 30  min Trade TYPE 2".format(trade_type,symbol,datetime.datetime.now()))
		#Checks if position is not already taken in the same side
		if not position_taken(symbol,strategy,trade_type,fyers):

			if trade_type == 'BUY':
				write_30min_log("--------------------------------------------------------")
				write_30min_log(" Start BUY Positions: 30 Min Trades (Type 2): {}".format(symbol))
				write_30min_log("--------------------------------------------------------")
				print(" Placing BUY order for 30 min BO Type 2...")
				print(" paramaters are trade_type:{} sl:{} qt1:{} Tp1:{}".format(trade_type,sl,quantity,tp1))
				write_30min_log("INFO:\tPlacing BUY order for 30 min BO Type 2...")
				write_30min_log("INFO:\tparamaters are trade_type:{} sl:{} qt1:{} Tp1:{}".format(trade_type,sl,quantity,tp1))
				try:
					response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp1,quantity,fyers)
					if response is None:
						print(" order placement error")
						write_30min_log("ERROR:\tOrder Placement error")
					else:
						print("*** prder placed ***")
						write_30min_log("**** ORDER PLACED ****")

				except Exception as e:
					print(" ERROR: Order placement failed")
					print(e)
					write_30min_log("ERROR:\tOrder plaement failed in {}".format(symbol))
					write_30min_log(e)
				write_30min_log("--------------------- End of Order ---------------------\n")






			if trade_type == 'SELL':
				write_30min_log("--------------------------------------------------------")
				write_30min_log(" Start SELL Positions: 30 Min Trades (Type 2): {}".format(symbol))
				write_30min_log("--------------------------------------------------------")
				print(" Placing SELL order for 30 min BO Type 1...")
				print(" paramaters are trade_type:{} sl:{} qt1:{} Tp1:{}".format(trade_type,sl,quantity,tp1))
				write_30min_log("INFO:\tPlacing SELL order for 30 min BO Type 2...")
				write_30min_log("INFO:\tparamaters are trade_type:{} sl:{} qt1:{} Tp1:{} ".format(trade_type,sl,quantity,tp1))
				try:
					response=place_bracket_30min_order_MARKET(symbol,trade_type,sl,tp1,quantity,fyers)
					if response is None:
						print(" Order placement error")
						write_30min_log("ERROR:\tOrder placement error")
					else:
						print(" Order placed")
						write_30min_log("**** ORDER PLACED ****")
				except Exception as e:
					print(" ERROR: Order placement failed")
					print(e)
					write_30min_log("ERROR:\t Order plaement failed in {}".format(symbol))
					write_30min_log(e)
				write_30min_log("--------------------------------------------------------\n")
				
		else:
			print(" Already in Position")
			write_30min_log("INFO:\t Already in position for {}".format(symbol))








































d