from collections import deque
from datetime import datetime


class Attempts(deque):
    def __init__(self, iterable=None, maxlen=10):
        if not iterable:
            iterable = tuple()
        super().__init__(iterable, maxlen)

    def get_by_username(self, username: str, default=None):
        for item in self:
            if item == username:
                return item
        return default

    def update(self, username, password=None, timestamp=None, peername=None):
        item = self.get_by_username(username)
        if item:
            self.remove(item.username)
            if password:
                item.password = password
            if timestamp:
                item.timestamp = timestamp
            if peername:
                item.peername = peername
        else:
            item = Attempt(username, password, timestamp, peername)
        self.append(item)
        return item


class Attempt:
    def __init__(self, username, password=None, timestamp=None,
                 peername=None):
        self.username: 'str' = username
        self.password: 'str' = password
        self.timestamp: 'datetime' = timestamp
        self.peername: 'str' = peername

    def __eq__(self, username):
        return self.username == username

    def __repr__(self):
        return 'CacheItem(' \
               f'username={self.username}, ' \
               f'password={self.password}, ' \
               f'timestamp={self.timestamp}, ' \
               f'peername={self.peername})'


attempts = Attempts()
