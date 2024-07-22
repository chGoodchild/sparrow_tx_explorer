import requests

url = 'https://api.coindesk.com/v1/bpi/historical/close.json'
params = {
    'start': '2023-01-01',
    'end': '2023-01-31'
}
response = requests.get(url, params=params)
data = response.json()

print(data)
