import math
from threading import Thread
import weakref

from xmlrpc.client import ServerProxy, Fault


class NaoqiClientAgent(object):
    '''ClientAgent request RPC service from remote server
    '''
    # YOUR CODE HERE
    def __init__(self, server_uri='http://172.17.0.3:8000'):
        self._server_proxy = ServerProxy(server_uri, allow_none=True)

    def stand_init(self):
        try:
            self._server_proxy.stand_init()
        except Fault:
            pass

    def moveTo(self, x, y, theta=math.pi/2.0):
        self._server_proxy.moveTo(x, y, theta)

    def rest(self):
        try:
            self._server_proxy.rest()
        except Fault:
            pass

if __name__ == '__main__':
    agent = NaoqiClientAgent()

    agent.stand_init()
    agent.moveTo(0.3, 0.1)
    print('Done')
