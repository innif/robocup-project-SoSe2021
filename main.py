import logging
import math
from threading import Thread
from PIL import Image

from cv_agent import CVAgent
from walking_agent import WalkingAgent


def main():
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger(__name__)

    # Set server uri of naoqi rpc server
    server_ip_address, server_port = '172.17.0.2', 8000
    server_uri = "http://{}:{}".format(server_ip_address, server_port)

    walking_agent = WalkingAgent(server_uri=server_uri)
    cv_agent = CVAgent(server_uri=server_uri)

    logger.info('walking_agent started')

    nao_image = cv_agent.get_image()
    image_width = nao_image[0]
    image_height = nao_image[1]
    array = nao_image[6]
    image_string = bytes(array, encoding='ascii')

    # Create a PIL Image from our pixel array.
    im = Image.frombytes("RGB", (image_width, image_height), image_string)

    # Save the image.
    im.save("camImage.png", "PNG")

    im.show()

    walking_agent.walk_to(1, -0.50, 0, wait=True)
    logger.info('Finished')


if __name__ == '__main__':
    main()
