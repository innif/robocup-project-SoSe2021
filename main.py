import logging

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

    img = cv_agent.get_image()
    cv2.imwrite("vision.png", img)

    logging.info('walking started')
    walking_agent.walk_to(1, -0.50, 0)
    logging.info('Finished')


if __name__ == '__main__':
    main()
