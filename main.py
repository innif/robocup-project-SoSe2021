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


if __name__ == '__main__':
    main()
