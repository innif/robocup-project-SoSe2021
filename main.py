import argparse
import logging
import math

from cv_agent import CVAgent
from walking_agent import WalkingAgent
from navigation_agent import NavigationAgent


def main(naoqi_ip, naoqi_port):
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger(__name__)

    server_ip_address, server_port = naoqi_ip, naoqi_port
    server_uri = "http://{}:{}".format(server_ip_address, server_port)

    navigation_agent = NavigationAgent(server_uri=server_uri)

    logger.info('Start looped procedure to turn robot and walk to goal.')

    navigation_agent.cv_agent.update()

    input("type anything")
    while True:
        navigation_agent.run()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)

    args = parser.parse_args()

    return args.ip, args.port


if __name__ == '__main__':
    main(*parse_args())
