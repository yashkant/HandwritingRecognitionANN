import requests


pincode = 442401
resp = requests.get("https://pincode.saratchandra.in/api/pincode/"+str(pincode))


if(resp.json()['status'] == 200):
	data = (resp.json())['data']
	print data[0]['taluk']
else:
	print 'Not a valid pincode' 	