# anm
Makes the login & command sending of Netmiko asynchron to speed up things.

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

while True:
    if a.exec_done and b.exec_done:
        print(a.exec_done)
        print(b.exec_done)
```
