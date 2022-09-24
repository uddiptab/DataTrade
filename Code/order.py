import pandas as pd 
import numpy as np
from fyers_api import fyersModel
from fyers_api import accessToken
import datetime
import time

#######################################
# Initialization
######################################
client_id="8P1AKSLX1V-100"
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
	file.write(datetime.datetime.now()+": "+text+"\n")
	file.close()





##########################################################
# Main Loop (divided into two parts)
	# 1. One time data collection for candle based strategies
	# 2. Keep getting live data feed and historical data for MA strategies
##########################################################

#Scrips for which data to be collected (other than NIFTY/BNF/CURRENCy,COMMODITY)
# Change Currency/commodity derivatives once in a month
scrip_list=['SBIN','INFY']



# Declare the dict to hold the previous ltp
prev_ltp={}


#Timer inti to keep track of 5 min passed/15 min passed/1 hour passed
time_5min=time.time()
time_15min=time.time()
time_1hour=time.time()






for i in range (0,10):
	print(" Debug: in the loop")
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
	prevdate=datetime.datetime.today()-datetime.timedelta(days=1)
	prevdate=prevdate.strftime("%Y-%m-%d")
	print(curdate,prevdate)


	if not JPY_2ND_CANDLE_FLAG:
		if (hour==14 and minute>=30) or (hour>=15):
			data = {"symbol":"NSE:JPYINR22SEPFUT","resolution":"60","date_format":"1","range_from":"2022-09-21","range_to":"2022-09-22","cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			#print(df)
			df.to_csv('../Data/Intraday/1hour/JPYINR.csv',index=False)
			log_write(" DATACOLLECTION: JPY 2nd candle data collected...")
			JPY_2ND_CANDLE_FLAG=True
	if not GBP_3rd_CANDLE_FLAG:
		if (hour==15 and minute>=30) or (hour>=16):
			data = {"symbol":"NSE:GBPINR22SEPFUT","resolution":"60","date_format":"1","range_from":"2022-09-21","range_to":"2022-09-22","cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			#print(df)
			df.to_csv('../Data/Intraday/1hour/GBPINR.csv',index=False)
			log_write("DATACOLLECTION: GBP 3rd candle data connected...")
			GBP_3rd_CANDLE_FLAG=True
	if not BN_30_MIN_FLAG:
		if (hour==16 and minute>=15) or (hour>=17):
			data = {"symbol":"NSE:NIFTYBANK-INDEX","resolution":"60","date_format":"1","range_from":"2022-09-21","range_to":"2022-09-22","cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			#print(df)
			df.to_csv('../Data/Intraday/30min/JBNF.csv',index=False)
			log_write(" DATACOLLECTION: BNF 12:45 candle data collected (12:15-12:45")
			BN_30_MIN_FLAG=True


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

	if time.time()-time_5min>300:
		#Collect BNF dta firsts
		data = {"symbol":"NSE:NIFTYBANK-INDEX","resolution":"5","date_format":"1","range_from":"2022-09-21","range_to":"2022-09-22","cont_flag":"1"}
		dt=fyers.history(data)
		df=convert_data_to_df(dt)
		df.to_csv('../Data/Intraday/5min/BNF.csv',index=False)
		log_write(" DATACOLLECTION: BNF 5 min data collected...")
		#Collect stocks data
		for stocks in scrip_list:
			symbol="NSE:"+stocks+"-EQ"
			data = {"symbol":symbol,"resolution":"5","date_format":"1","range_from":"2022-09-21","range_to":"2022-09-22","cont_flag":"1"}
			dt=fyers.history(data)
			df=convert_data_to_df(dt)
			df.to_csv('../Data/Intraday/5min/'+stocks+'.csv',index=False)
			log_write(" DATACOLLECTION: {} 5 min data collected...".format(stocks))

		#reseting the timer
		time_5min=time.time()
			

	if time.time()-time_15min>900:
		#Collect BNF dta firsts
		data = {"symbol":"NSE:NIFTYBANK-INDEX","resolution":"15","date_format":"1","range_from":"2022-09-21","range_to":"2022-09-22","cont_flag":"1"}
		dt=fyers.history(data)
		df=convert_data_to_df(dt)
		df.to_csv('../Data/Intraday/15min/BNF.csv',index=False)
		log_write(" DATACOLLECTION: BNF 15 min candle data collected...")
		#resetting the timer
		time_15min=time.time()


	##############################################
	# Live market quote fetch
	# This part continiously fetches ltp for isntruments
	# Then check for entry conditions
	#############################################
	












	time.sleep(100)

		



















