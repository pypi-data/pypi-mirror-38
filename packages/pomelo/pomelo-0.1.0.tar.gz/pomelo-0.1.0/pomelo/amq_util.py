import stomp
import functools
import time
import zk_util
import json
import logging

class AMQListener(object):
    def __init__(self,fun):
        self._fun = fun
    def on_message(self, headers, message):
        self._fun(headers,message)

    def on_error(self, headers, message):
        print(headers)
        print(message)

class AMQUtil(object):
    def __init__(self,ip,port,user,passwd):
        self._ip = ip
        self._port = port
        self._user = user
        self._passwd = passwd
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
        self.client = stomp.Connection10([(self._ip,self._port)])
        self.client.start()
        self.client.connect(login=self._user, passcode=self._passwd)
    
    @connect_required
    def send2queue(self,qname,msg):
        self.client.send(qname,msg)

    @connect_required
    def send2topic(self,ttopic,msg):
        self.client.send(ttopic,msg)

    @connect_required
    def recvmsg(self,qname,fun):
        self.client.set_listener('Listener', AMQListener(fun))
        self.client.subscribe(qname, ack='auto', transformation="jms-json")

    def __del__(self):
        if (self.client):
            self.client.disconnect()
    
def AMQCluster(object):
    def __init__(self,zk,ips,dev_user,dev_pass,adm_user,adm_pass):
        self._zk = zk
        self._ips = ips
        self._dev_user = dev_user
        self._dev_pass = dev_pass
        self._adm_user = adm_user
        self._adm_pass = adm_pass
    def get_master(self):
        zkobj = zk_util.ZKUtil(zk)
        t = zkobj.children('/activemq/leveldb-stores')
        for k in t:
            m = zkobj.get('/activemq/leveldb-stores/' + k)
            dt = json.loads(m[0].decode())
            logging.debug("address:{},elected:{}".format(dt["address"],dt["elected"]))
            if (dt["address"] != None):
                logging.info(dt["address"])
                for ip in self._ips:
                    if (dt["address"].find("tcp://{}:".format(ip)) >= 0):
                        return ip
        return None
    def check(self):
        master = self.get_master()
        if (master == None):
            logging.info("not found master,zk:%s,ips:%s",self._zk,self._ips)
            return
        obj = AMQUtil(master,61613,self._dev_user,self._dev_pass)
        flag = True
        def fun(header,msg):
            logging.info("header:%s,msg:%s",header,msg)
            flag = False
        cnt = 0
        obj.recvmsg('/queue/test1',fun)
        obj.send2queue('/queue/test1','test1233')
        while flag or cnt < 5:
            cnt = cnt + 1
            time.sleep(1)
        if (flag == False):
            return True,master
        else:
            return False,''


if __name__ == '__main__':
    obj = AMQUtil('10.130.9.123',61613,'XXXX','XXXXX')
    def fun(header,msg):
        print(header)
        print(msg)    
    obj.recvmsg('/queue/test1',fun)
    while True:
        obj.send2queue('/queue/test1','test1233')
        time.sleep(1)


