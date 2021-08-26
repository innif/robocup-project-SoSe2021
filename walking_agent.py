# Sebastian
from robolib import NaoqiClientAgent

class WalkingAgent:
    def __init__(self, server_uri):
        self._agent = NaoqiClientAgent(server_uri=server_uri)

    def walk_to(self, x, y, theta=0.0, wait=True):
        """
        Walk to x and y coordinates
        @param x: x coordinate
        @param y: y coordinate
        @param theta: rotation in radians around the robots own axis
        @param wait: make the call run async or not
        """
        self._agent.moveTo(x, y, theta, run_async=(not wait))
