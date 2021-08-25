# Finn
from robolib.pynaoqi_wrapper import vision_definitions
from robolib import NaoqiClientAgent


class CVAgent:
    def __init__(self, server_uri):
        self._agent = NaoqiClientAgent(server_uri)
        self.goal_center = (100, 100)  # Center of Goal in Pixels
        self.goal_size = (100, 200)  # width, height

        resolution = vision_definitions.kQQVGA
        color_space = vision_definitions.kRGBColorSpace
        self._agent.subscribe_to_cam(resolution, color_space)

    def update(self, perception) -> None:
        pass

    def get_image(self):
        return self._agent.get_image()
