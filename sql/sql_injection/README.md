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
<br>

## SQL Features
#### `UNION` : Link multiple `select`
> Cautions : <li> Result of each linked `select` should have same number of columns. </li>  
> <li> The data type of each linked `select` should same with each other.(applied only some dbms like mssql) </li>  
####  : 
