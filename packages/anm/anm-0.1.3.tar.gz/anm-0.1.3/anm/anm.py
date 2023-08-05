import asyncio

from netmiko import ConnectHandler
from threading import Thread


class NetworkDevice():
    def login(self):
        self.loop = asyncio.new_event_loop()

        def f(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        thread = Thread(target=f, args=(self.loop,))
        thread.start()
        asyncio.run_coroutine_threadsafe(self.async_login(), self.loop)

    async def async_login(self):
        try:
            self.con = ConnectHandler(**{
                'device_type': self.device_type,
                'ip': self.ip,
                'username': self.username,
                'password': self.password
            })
            self.session = True
        except:
            self.session = False
            self.error = 'Login Error'
        self.loop.call_soon_threadsafe(self.loop.stop)

    def __init__(self, ip, username, password, device_type='cisco_ios'):
        self.ip = ip
        self.username = username
        self.password = password
        self.device_type = device_type
        self.session = False
        self.con = None
        self.loop = None
        self.error = False