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


## NoSQL injection : 
