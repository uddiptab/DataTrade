from fyers_api import fyersModel
from fyers_api import accessToken
import time
import webbrowser


def login():
	'''
	Logs in the user and finally writes the access token in the file
	'''
	client_id="H8O8SRR6U6-100"
	secret_key="WA58YUMWLM"
	session=accessToken.SessionModel(client_id=client_id, secret_key=secret_key,redirect_uri="https://trade.fyers.in",grant_type="authorization_code",response_type="code")
	print(" Open the Login screen in the browser...")
	print(session.generate_authcode() )
	value=input("Please enter your auth code:")
	value=str(value)
	auth_code=value
	session.set_token(auth_code)
	response = session.generate_token()
	access_token=response["access_token"]
	file=open('../Input/token.txt','w')
	file.write(str(access_token))
	file.close()
	print("\n accessToken written to the file ...")


login()