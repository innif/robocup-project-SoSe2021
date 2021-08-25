import logging

from cv_agent import CVAgent
from walking_agent import WalkingAgent
from navigation_agent import NavigationAgent


def main():
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    
    server_ip_address, server_port = '127.0.0.1', 8000
    server_uri = "http://{}:{}".format(server_ip_address, server_port)
    
    navigation_agent = NavigationAgent(server_uri=server_uri)

    logging.info('Start looped procedure to turn robot and walk to goal.')
    
    while True:
        navigation_agent.run()

def main_o():
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger(__name__)

    # Set server uri of naoqi rpc server
    server_ip_address, server_port = '127.0.0.1', 8000
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
