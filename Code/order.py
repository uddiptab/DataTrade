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

def convert_data_to_df(data):
	'''
	Takes the output data and converts it to dataframe
	'''
	df=pd.DataFrame(columns=['TS','O','H','L','C','VOL'])
	candle_list=data['candles']
	for candle in candle_list:
		i=len(df)
		df.loc[i]=candle
	return df

def log_write(text):
	'''
	Writes in the Log file
	'''
	today = datetime.date.today()
	date=today.strftime("%Y-%m-%d")
	file=open('../Log/'+date+'_datacollect.txt','a')
	text1=("{}: ".format(datetime.datetime.now()))
	file.write(text1+text+"\n")
	file.close()





##########################################################
# Main Loop (divided into two parts)
	# 1. One time data collection for candle based strategies
	# 2. Keep getting live data feed and historical data for MA strategies
##########################################################

T30_min_data_collected=False
#Scrips which will be evaluated for first red candle short
first_red_scrip_list=[] # This list holds all the stocks for which First red candle strategy will be evaluated (Input from Keyboard)
print(" Enter 5 stocks for which First red candle strategy will be evaluated...")
print(" Enter stock symbols separated by space. Eg TCS INFY SBIN. Press NA if you don't want to add any...")
first_red_scrip_list= list(map(str,input("\n Enter the stocks: ").split()))
if len(first_red_scrip_list)>1:
	df= pd.DataFrame({'STOCKS':first_red_scrip_list})
	df.to_csv('../Input/red_candle_short_stocks.csv')
	print(" Red candle short stock lists updated...")
	log_write(" Red candle short stock lists updated...")

# Scrip list is the list that holds all stocks to be checked
scrip_list=[]

# Add red candle stocks to the scrip list
for stock in first_red_scrip_list:
	scrip_list.append(stock)

quote_stock_list=["NSE:NIFTY50-INDEX","NSE:NIFTYBANK-INDEX"]
for stock in scrip_list:
	quote_stock_list.append("NSE:"+stock+"-EQ")





# Declare the dict to hold the previous ltp
prev_ltp={}
#initialize prev ltp
for scrip in quote_stock_list:
	prev_ltp[scrip]=None




######################
# For 30 min entries
######################
stock_list1 = ['BAJFINANCE','SBIN'] #30 min breakout max 2 entry tp1 = 2*diff tp2  = 3*diff
stock_list2 = ['TCS','SUNPHARMA','RELIANCE','MARUTI'] # Max 2 tnry // Hold for the entire day
quote_list=[]
for stock in stock_list1:
	quote_list.append('NSE:'+stock+"-EQ")
for stock in stock_list2:
	quote_list.append('NSE:'+stock+"-EQ")

for symbol in quote_list:
	prev_ltp[symbol]=None





#Timer inti to keep track of 5 min passed/15 min passed/1 hour passed
time_5min=time.time()
time_15min=time.time()
time_1hour=time.time()




#Loop
#for i in range (0,50):
while True:
	#print(" Debug: in the loop")
	# Flag to check if BN 12:45 30 min candle details is recorded (see strategy details at:)
	BN_30_MIN_FLAG=False
	# JPYINR second one hour data collecttion flag
	JPY_2ND_CANDLE_FLAG=False
	#GBPINR 3rd one hour candle data collection flags
	GBP_3rd_CANDLE_FLAG=False

	# Getting current time
	hour=datetime.datetime.now().hour
	minute=datetime.datetime.now().minute

	#Getting current date and previous date (for historical data collection purpose)
	curdate=datetime.datetime.today()
	curdate=curdate.strftime("%Y-%m-%d")
	prevdate=datetime.datetime.today()-datetime.timedelta(days=4)
	prevdate=prevdate.strftime("%Y-%m-%d")
	

	'''
	if not JPY_2ND_CANDLE_FLAG:
		if (hour==14 and minute>=30) or (hour>=15):
			data = {"symbol":"NSE:JPYINR22SEPFUT","resolution":"60","date_format":"1","range_from":curdate,"range_to":curdate,"cont_flag":"1"}
			dt=fyers.history(data)
			print("------------")
			print(dt)
			df=convert_data_to_df(dt)
			#print(df)
			df.to_csv('../Data/Intraday/1hour/JPYINR.csv',index=False)
			log_write(" DATACOLLECTION: JPY 2nd candle data collected...")
			JPY_2ND_CANDLE_FLAG=True
	if not GBP_3rd_CANDLE_FLAG:
		if (hour==15 and minute>=30) or (hour>=16):
			data = {"symbol":"NSE:GBPINR22SEPFUT","resolution":"60","date_format":"1","range_from":curdate,"range_to":curdate,"cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			#print(df)
			df.to_csv('../Data/Intraday/1hour/GBPINR.csv',index=False)
			log_write("DATACOLLECTION: GBP 3rd candle data connected...")
			GBP_3rd_CANDLE_FLAG=True
	if not BN_30_MIN_FLAG:
		if (hour==16 and minute>=15) or (hour>=17):
			data = {"symbol":"NSE:NIFTYBANK-INDEX","resolution":"60","date_format":"1","range_from":curdate,"range_to":curdate,"cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			#print(df)
			df.to_csv('../Data/Intraday/30min/JBNF.csv',index=False)
			log_write(" DATACOLLECTION: BNF 12:45 candle data collected (12:15-12:45)")
			BN_30_MIN_FLAG=True
	'''


	################################################
	# Keep Collecting Data for continious candles
	################################################

	###############################
	# Algorithm
	#	1. START loop
	#	2. START Data Collection module to manage data collection for different strategies
	#		3. Collect BN data for every 5 min until first red candle appears (see: startegy)
	#		4. Collect 5 min data for Gap up opening stocks (First 5) for 5 EMA
	#		5. Keep collecting 15 min Bank nifty data for 5 EMA strategy and Inside candle
	#	5. END Data collection module
	#	6. START Live quote module
	#		7. Check entry and redirect
	#		8. Update the previous ltp dict
	#	9. END live market quote
	#################################
	FIRST_RED_CANDLE_SEEN_FLAG=False

	if time.time()-time_5min>300:
		#Collect BNF dta firsts 5 min red candle
		if not FIRST_RED_CANDLE_SEEN_FLAG:
			pass
			'''
			try:
				data = {"symbol":"NSE:NIFTYBANK-INDEX","resolution":"5","date_format":"1","range_from":curdate,"range_to":curdate,"cont_flag":"1"}
				dt=fyers.history(data)
				df=convert_data_to_df(dt)
				last_open=df.iloc[-1,1]
				last_close=df.iloc[-1,3]
				#Stop the data collection once red candle seen
				if last_open-last_close>0:
					print(" First red candle seen...")
					df.to_csv('../Data/Intraday/5min/BNF.csv',index=False)
					log_write(" DATACOLLECTION: BNF 5 min data collected...")
					FIRST_RED_CANDLE_SEEN_FLAG=True
			except Excpetion as e:
				print(e)
			# Getting the bankbees data
			
			data = {"symbol":"NSE:BANKBEES-EQ","resolution":"5","date_format":"1","range_from":"2022-09-21","range_to":"2022-09-22","cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			df.to_csv('../Data/Intraday/5min/BANKBEES-EQ.csv',index=False)
			log_write(" DATACOLLECTION: Bankbees 5 min data collected...")
			'''


		else:
			print("Green candle seen...NIFTYBANK")




		#Collect stocks data (5 min candles)
		for stocks in scrip_list:
			symbol="NSE:"+stocks+"-EQ"
			data = {"symbol":symbol,"resolution":"5","date_format":"1","range_from":curdate,"range_to":curdate,"cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			df.to_csv('../Data/Intraday/5min/'+stocks+'.csv',index=False)
			print(" Data collected for {} {}".format(stocks,symbol))
			log_write(" DATACOLLECTION: {} 5 min data collected...".format(stocks))

		#reseting the timer
		time_5min=time.time()
			





	if time.time()-time_15min>900:
		
		#Collect BNF dta firsts
		data = {"symbol":"NSE:NIFTYBANK-INDEX","resolution":"15","date_format":"1","range_from":prevdate,"range_to":curdate,"cont_flag":"1"}
		dt=fyers.history(data)
		df=convert_data_to_df(dt)
		df.to_csv('../Data/Intraday/15min/BNF.csv',index=False)
		log_write(" DATACOLLECTION: BNF 15 min candle data collected...")

		#resetting the timer
		time_15min=time.time()

		#Data collection especially for only NIFTY 12:45 strategy
		if datetime.datetime.now().hour==16 and datetime.datetime.now().minute>=15 and datetime.datetime.now().minute<25:
			data = {"symbol":"NSE:NIFTY50-INDEX","resolution":"30","date_format":"1","range_from":prevdate,"range_to":curdate,"cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			df.to_csv('../Data/Intraday/30min/NIFTY1245.csv',index=False)
			log_write(" DATACOLLECTION: NIFTY 12:45 candle data collected...")

			data = {"symbol":"NSE:NIFTYBEES-EQ","resolution":"30","date_format":"1","range_from":prevdate,"range_to":curdate,"cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			df.to_csv('../Data/Intraday/30min/NIFTYBEES1245-EQ.csv',index=False)
			log_write(" DATACOLLECTION: NIFTYBEES   12:45 candle data collected...")



	##############################################
	# Live market quote fetch
	# This part continiously fetches ltp for isntruments
	# Then check for entry conditions
	#############################################

	
	for stock in quote_stock_list:
		data = {"symbols":stock}
		quotes=fyers.quotes(data)
	
		ltp=quotes['d'][0]['v']['lp']
		print("Stock:{} LTP:{}".format(stock,ltp))
		pltp=prev_ltp[stock]


		# Check for any entry/exit signal
		try:
			et.check_entry(stock,ltp,pltp,fyers)
		except Exception as e:
			print(e)
			log_write(" Error in data collection...")

		#Update the dictionary
		prev_ltp[stock]=ltp
	


	####################################
	# data Collection 30 min
	###################################
	



	#Collect the data after one hour
	if (datetime.datetime.now().hour == 13 and datetime.datetime.now().minute==45) or (datetime.datetime.now().hour == 14 and datetime.datetime.now().minute==45):

		for stock in quote_list:
			
			data = {"symbol":stock,"resolution":"30","date_format":"1","range_from":curdate,"range_to":curdate,"cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			fname=stock[4:-3]
			df.to_csv('../Data/Intraday/30min/'+fname+'.csv',index=False)
		

		time.sleep(2)
		
	####################################
	# For 30 min breakout stock
	####################################
	if (datetime.datetime.now().hour==13 and datetime.datetime.now().minute>=45) or (datetime.datetime.now().hour>=14):
		print(" \n\n### BO STOCVK #######")
		stock_list1 = ['BAJFINANCE','SBIN'] #30 min breakout max 2 entry tp1 = 2*diff tp2  = 3*diff
		stock_list2 = ['TCS','SUNPHARMA','RELIANCE','MARUTI'] # Max 2 tnry // Hold for the entire day
		quote_list=[]
		for stock in stock_list1:
			symbol="NSE:"+stock+"-EQ"
			data = {"symbols":symbol}
			quotes=fyers.quotes(data)
			ltp=quotes['d'][0]['v']['lp']
			pltp=prev_ltp[symbol]
			print("Stock:{} LTP:{} prev_ltp:{}".format(symbol,ltp,pltp))
			try:
				et.check_30min_type1(symbol,ltp,pltp,fyers)
			except Exception as e:
				print(e)
			prev_ltp[symbol]=ltp

		for stock in stock_list2:
			symbol="NSE:"+stock+"-EQ"
			data = {"symbols":symbol}
			quotes=fyers.quotes(data)
			ltp=quotes['d'][0]['v']['lp']
			print("Stock:{} LTP:{}".format(symbol,ltp))
			pltp=prev_ltp[symbol]
			print("Stock:{} LTP:{} prev_ltp:{}".format(symbol,ltp,pltp))
			try:
				et.check_30min_type2(symbol,ltp,pltp,fyers)
			except Exception as e:
				print(e)
			prev_ltp[symbol]=ltp

	time.sleep(10)

		



















