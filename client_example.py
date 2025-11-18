import requests

print("呼叫 API")

server_url = "http://localhost:8000"
symbol = 2330
method = "neuralprophet"
response = requests.get(f"{server_url}/api/v1/stocks/{symbol}/prediction?method={method}").json()

print("明天是", response['neuralprophet']['next_day'])
print(method, "預測", symbol, "的價格是", response['neuralprophet']['price'])
