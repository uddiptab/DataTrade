import pandas as pd 
import numpy as np
import strategy as st
import datetime
import time


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


def position_taken_bracket(symbol,trade_type,fyers):
	'''
	Checks if a bracket order is open 
	Input: filename order of the bracket order details
	Strategy Name of the strategy
	'''
	

def place_buy_bracket_order(symbol,trade_type,sl,tp,quantity,strategy):
	'''
	Place a BUY bracket order with params
	Write details with the name of the strategy in the transaction file
	'''
	pass


def position_taken(symbol,strategy,entry_type,fyers):
	'''
	Checks if a particular position is already open
	1. Check if the SYMBOL is open in current positions
	2. Check from positions.csv
	3. Decide
	'''
	falg = False
	pos=fyers.positions()
	netPos=pos['netPositions']
	for trades in netPos:
		stock = trades['symbol']
		unrelProfit =trades['unrealized_profit']
		side = trades['side']

		if str(side) =='1':
			side = 'BUY'
		if str(side)==-1:
			side = 'SELL'
		if unrelProfit>0 and symbol ==stock and side == entry_type:
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
		first_red_short_stock_list = irst_red_short_stock_list_file['STOCKS'].values

		stock = symbol.split("-")[0]
		stock = stock[4:]
		print(" Checking details for:{} {}".format(symbol,stock))

		if stock in first_red_short_stock_list:
			flag,trade_type,strategy,quantity,qt1,qt2,sl,tp1,tp2 = st.first_red_candle_short(stock,ltp,prev_ltp)

			# If the signal comes out as true
			if flag:
			print("{} Signal generated in JPYINR at {}".format(trade_type,datetime.datetime.now()))
			#Checks if position is not already taken in the same side
			if not position_taken(symbol,strategy,trade_type):		
				elif trade_type == 'SELL':
					orderid=place_sell_order(symbol,trade_type,quantity)
					print("Placed sell order JPY.......")
					write_to_trade_tracker_file(orderid,symbol,trade_type,strategy,ltp,sl,quantity,qt1,qt2,tp1,tp2)
			else:
				print(" Already in Position")
				write_entry_log("{} Already in position\n".format(symbol))

		#2. For 5 min candle BO (Only for slected stocks)
		




























