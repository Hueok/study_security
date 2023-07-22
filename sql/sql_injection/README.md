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
> $regex : select document which corresponds with regular expression (more about regex : https://wooncloud.com/113#%EC%--%B-%EC%BB%A-%---Anchors-)
<br>

## SQL Features
#### `UNION` : Link multiple `select`
> Cautions : <li> Result of each linked `select` should have same number of columns. </li>  
> <li> The data type of each linked `select` should same with each other.(applied only some dbms like mssql) </li>  
#### `Subquery` : usage of inner query in a query.  
> We can access other table the query not take, by use it. Also, we can use `select` where it is not used.  
> Cautions :
> <li> Result of subquery should return __single row__ and __single column__ in the `columns` clause </li>  
> <li> Result of subquery can return __multiple row__ and __multiple columns__ in the `FROM` cluase</li>  
> <li> Result of subquery can return __multiple row__ in the `WHERE` clause</li>
#### `Applicaiton Logic`
> by analyzing logic of web application, we can attack with `union`, `if()` and etc.... <- whether logic has output or not is very important to us.
