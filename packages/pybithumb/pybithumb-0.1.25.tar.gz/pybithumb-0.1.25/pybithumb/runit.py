import requests

url = "https://api.bithumb.com/public/ticker/ALL"
resp = requests.get(url)
data = resp.json()
data = data['data']
keys = data.keys()

tickers = [k for k in keys if k is not 'date']
print(tickers)
