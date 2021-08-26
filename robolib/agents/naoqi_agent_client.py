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
        """
        Make init pose
        """
        try:
            self._server_proxy.stand_init()
        except Fault:
            pass

    def moveTo(self, x, y, theta=0.0, run_async=True):
        """
        Walk to x and y coordinates
        @param x: x coordinate
        @param y: y coordinate
        @param theta: rotation in radians around the robots own axis
        @param wait: make the call run async or not
        """
        self._server_proxy.moveTo(x, y, theta, run_async)

    def rest(self):
        """
        Return to rest pose
        """
        try:
            self._server_proxy.rest()
        except Fault:
            pass

    def waitUntilMoveIsFinished(self):
        """
        Wait until current walking movement is finished
        """
        try:
            self._server_proxy.waitUntilMoveIsFinished()
        except Fault:
            pass

    def subscribe_to_cam(self, resolution: int, color_space: int) -> None:
        """
        Subscribe to camera
        @param resolution: resolution of the camera
        @param color_space: color space of the camera
        """
        try:
            self._server_proxy.subscribe_to_cam(resolution, color_space)
        except Fault:
            pass

    def unsubscribe_from_cam(self) -> None:
        """
        Unsubscribe from camera
        """
        try:
            self._server_proxy.unsubscribe_from_cam()
        except Fault:
            pass

    def get_image(self) -> list:
        """
        Retrieve image
        """
        return self._server_proxy.get_image()


if __name__ == '__main__':
    agent = NaoqiClientAgent()

    agent.stand_init()
    agent.moveTo(1, 0)
    agent.waitUntilMoveIsFinished()
    print('Done')
