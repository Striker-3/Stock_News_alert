import requests

response = requests.get("https://financialmodelingprep.com/api/v3/search?query=AA&apikey=HemPBSRpXfBTAoIe9jojlPUSJWKkPGTB")
data = response.json()
print(data)