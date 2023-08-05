# anm
Makes the login (connection) process of Netmiko asynchron to speed up things.

## Simple Example
```python
from anm import NetworkDevice

a = NetworkDevice('10.0.0.1', 'admin', 'password')
b = NetworkDevice('10.0.0.2', 'admin', 'password')

a.login()
b.login()

while True:
    if a.session and b.session:
        print(a.con.send_command('sh version'))
        print(b.con.send_command('sh version'))
        break
```
