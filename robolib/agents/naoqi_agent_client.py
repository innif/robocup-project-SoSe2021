import math
import base64
from threading import Thread
import weakref

from xmlrpc.client import ServerProxy, Fault


class NaoqiClientAgent(object):
    '''ClientAgent request RPC service from remote server
    '''
    # YOUR CODE HERE
    def __init__(self, server_uri='http://172.17.0.3:8000'):
        self._server_proxy = ServerProxy(server_uri, allow_none=True, use_builtin_types=True)

    def stand_init(self):
        try:
            self._server_proxy.stand_init()
        except Fault:
            pass

    def moveTo(self, x, y, theta=0.0, run_async=True):
        self._server_proxy.moveTo(x, y, theta, run_async)

    def rest(self):
        try:
            self._server_proxy.rest()
        except Fault:
            pass

    def waitUntilMoveIsFinished(self):
        try:
            self._server_proxy.waitUntilMoveIsFinished()
        except Fault:
            pass

    def subscribe_to_cam(self, resolution: int, color_space: int) -> None:
        try:
            self._server_proxy.subscribe_to_cam(resolution, color_space)
        except Fault:
            pass

    def unsubscribe_from_cam(self) -> None:
        try:
            self._server_proxy.unsubscribe_from_cam()
        except Fault:
            pass

    def get_image(self) -> list:
        encoded_image = self._server_proxy.get_image()
        decoded_image = encoded_image[:6]
        decoded_image.append(encoded_image[6])
        return decoded_image


if __name__ == '__main__':
    agent = NaoqiClientAgent()

    agent.stand_init()
    agent.moveTo(1, 0)
    agent.waitUntilMoveIsFinished()
    print('Done')
