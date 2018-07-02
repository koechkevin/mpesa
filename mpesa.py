import requests
import json
import base64
response1 = requests.get("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",auth=('ygTnjAUKeMv1H7b2WmzjfgNDQJcEKNl9','Yr6RUbPBGRZGG8xs')).text
res=json.loads(response1)
access_token = res['access_token']
api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
headers = { "Authorization": "Bearer "+access_token}
timestamp="20180702180042"
shortcode="174379"
passkey="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
def passout(word):
    output=[]
    for each in str(base64.b64encode(bytes(word, 'utf-8'))).split('b\''):
        output.append(each.split("'"))
    return output[1][0]
	
    
password=passout(shortcode+passkey+timestamp)

ammount=int(input('enter ammount   '))
mobile=input('enter mobile in format 7XXXXXXXX   ')
request ={
      "BusinessShortCode": shortcode,
      "Password": password,
      "Timestamp": timestamp,
      "TransactionType": "CustomerPayBillOnline",
      "Amount": ammount,
      "PartyA": "254"+mobile,
      "PartyB": shortcode,
      "PhoneNumber": "254"+mobile,
      "CallBackURL": "http://mpesa-requestbin.herokuapp.com/1hx6r081",
      "AccountReference": "test",
      "TransactionDesc": "test"
    }

response = requests.post(api_url, json = request, headers=headers)

print (response.text)