# Finn
import base64

import cv2
import numpy as np

from robolib.pynaoqi_wrapper import vision_definitions
from robolib import NaoqiClientAgent


class CVAgent:
    def __init__(self, server_uri):
        self._agent = NaoqiClientAgent(server_uri)
        self.goal_center = (100, 100)  # Center of Goal in Pixels
        self.goal_size = (100, 200)  # width, height

        resolution = vision_definitions.kQVGA
        color_space = vision_definitions.kRGBColorSpace
        self._agent.subscribe_to_cam(resolution, color_space)

    def update(self, perception) -> None:
        pass

    def get_image(self):
        nao_image = self._agent.get_image()
        img_decoded = base64.b64decode(nao_image[6])
        img = (np.reshape(np.frombuffer(img_decoded, dtype='%iuint8' % nao_image[2]),
                          (nao_image[1], nao_image[0], nao_image[2])))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img
