import requests

url = 'http://host3.dreamhack.games:23703'
test_url = 'https://bdqbwly.request.dreamhack.games'
param={
    'cmd' : 'test'
}

resp = requests.get(test_url, params = param).text

print(resp)