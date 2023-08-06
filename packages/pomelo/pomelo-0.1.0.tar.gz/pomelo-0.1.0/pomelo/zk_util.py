from kazoo.client import KazooClient
from kazoo.client import KazooState
import functools
import json

class ZKUtil(object):
    def __init__(self,hosts):
        self._hosts = hosts
        self.client = None

    def connect_required(func):
        @functools.wraps(func)
        def handle_func(*args, **kwargs):
            self = args[0]
            if (not self.client):
                self.connect()
            rt = func(*args, **kwargs)
            return rt
        return handle_func    

    def connect(self):
        self.client = KazooClient(self._hosts, timeout = 10)
        self.client.start()

    @connect_required
    def get(self,path):
        return self.client.get(path)
    
    @connect_required
    def children(self,path):
        return self.client.get_children(path)


if __name__ == '__main__':
    z = ZKUtil('10.130.9.127:2181')
    t = z.children('/activemq/leveldb-stores')
    print(t)
    for k in t:
        m = z.get('/activemq/leveldb-stores/' + k)
        dt = json.loads(m[0].decode())
        print("address:{},elected:{}".format(dt["address"],dt["elected"]))

