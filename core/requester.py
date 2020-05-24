import requests
import json
from random import randint
from time import sleep
import os.path

excluded_addresses = [
"1Ptv5qNTg6bpoMrH8zKqpiSA62jC3i76Nr",
"3BTTDAn8HrmS2Lx48EoJy6v35B4jvAUW8p",
"3MpRwW1Z3QRbmhcQCHQkigUzJV4RApkguT",
"3FhmrEePt1UJ1dDZLQSVw4ku3ESUp2Ej4U"
]

known_addresses = [
#inputs
"3KGr5cStWHTohMPL9xeHFYzzu98ejoBcbs",
"3855Ym4LxXvXWpsaCVL8UUn7QZDhC3yikw",
"3KCFcShQBHudyyTSUznn9W2d1MYcBjvSk5",
"3FCJdhwLUSAyePxb823wAZCAbimAsAZLi7",
"39GAs8N1NhHpvmE4hefc39ihvAiFX2kUFm",
"31wrujVVhf92puvwe4uE1cDgKNc4gXuQRz",
"3KJzCfav5f9Cw8jpMQWWzM8viYC9Hsbz4h",
# outputs
"1BgJMzNobfa2vQU8is6c8pgDatVaVG5fXr",
"1NcVbCiDYB3A5Fxf5JPftRxTtSzkmjBNem",
"1Gf4sfkxSDVj93U5gNRwPYwAjYfg1ykxbY",
"15k8U8PFQifuu134x46SnocQRAkV7UQUAT",
"13b6zfnUHT8MYAo4oWT5gWBEJfeN6sRekD",
"1N1GxHSewXrvvFjaR1s88Wb2hyRPWMr36D",
"3Df2M6wirUdK1M5tLRN4ZiUGD4S6gDhyiD",
"17KHoTcFh4bPpY1wgUbANwV7MQLsH9Nd9e",
"3L3JVZnpLcWzqMtQ3SMFnc23CCmy331bqB",
"3LP79dNuxywCCwzcPy6eydxm46wwjKWzyn",
"3PuausFEYhUzC14SYGeiwVMPzP1BUbFRB4",
"3KsPS2vnaew8K8byn3WgRiu2eiqdwiKgsf",
"3BB3yGAqEaeQYjaRpjkjpcWo7qg1PG2eSW",
"1M4bdFnwKZPeyJFY5QT5pyqAZxmUBD9297", #duda
"17LnBqLqBgs35xSDp9N83RFoE2zH9ae2eA", #duda
"3Myp4jrkw2Tfe4tFMYifjV6gzwH6zQ6cwx", # cta de exchange que se usa desde antes del robo
"3MX15SzXQ4w6W7ieWCrVPJiCtcxXgHNVvx", # 6 btc 9 de mayo
"3PqCC1AYx9T1A9WVHp4E96kxqnpmwdu72j", # importante 18.26 btc el 8 de mayo
"3MxjKp16mf4eho4nRtDBrf3ei6DPSvEtxo", # importante 11.65 btc el 8 de mayo
"3L5qT5fAh3PHtLFhhaqt7cgJRTnWTFn7Ev", # importante 18.849 btc el 8 de mayo
"3E6e6vTj8sPJiZuw4sYpvT5Tc4DxFirn5Z", # importante 22 btc el 8 de mayo
"3B7mJkGGMgFY51kykg6kim3sHvLq1pAfpP", # importante 22.5 btc el 8 de mayo
"3EgDFKV7DwPbUiND1iMmmpSAFcAZLmmCXa", # importante 17.67 btc el 8 de mayo
"3Hwm278sfkzNNpczFHiJJgCGBPwXrDDLFy", # importante 26 btc el 8 de mayo
"3AgXamXPGs2JHQ6vM91PLMYnjPgBY6koe5", # importante 16 btc el 8 de mayo
"3DiaC96RxBzG5MRmfU2CiQCns139nqNVEY", # importante 38 btc el 8 de mayo
"17JmW6qpyrTnMeJYYinBnnqC1ioYbF2NiA", #binance
"1QBPLqjPARbsKgn4gBaeF8GUR1u8QMJ8zL", #binance
"1P1CQm4yqpJRC9VnTwo2WoqUtBkBBDFDVX", #binance
"19sjz7VuazJ8wLggZZM2po2c6gvXp6cg48", #binance
"1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1s" #binance ppal (por esta sabemos que las otras son de binance)
]

# https://api.blockchain.info/haskoin-store/btc/address/3J8zSiUeVxpZKRcZZXXF2KzKe3hAbZaiEY/transactions/full?limit=5&offset=5
def requester(url):
	if url in known_addresses:
		return ""

	p = 'cache/inputs/' + url + '.txt'
	if os.path.exists(p):
		# print ('path exist\n')
		file = open(p, mode='r')
		data = json.loads(file.read())
		file.close()
	else:
		# print ('path does not exist\n')
		sleep(randint(1, 2))
		data = requests.get('https://api.blockchain.info/haskoin-store/btc/address/' + url + '/transactions/full').json()
		file = open(p, mode='a')
		file.write(json.dumps(data) + "\n")
		file.close()

	# print ('address %s\n' % url)
	# print ('data before %s\n\n\n' % json.dumps(data))
	for tx in data:
		# print ('tx before %s\n' % json.dumps(tx))
		is_withdraw = False;
		for input in tx['inputs']:
			if input['address'] == url :
				is_withdraw = True;

		if is_withdraw:
			if len(tx['outputs']) > 2 and not url in excluded_addresses:
				return "" #"is exchange"
			del tx['inputs']

		del tx['outputs']
		# print ('tx after %s\n\n\n' % json.dumps(tx))

	# print ('data after %s\n\n\n' % json.dumps(data))
	return json.dumps(data).replace("'", '"')
