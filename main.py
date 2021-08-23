import logging
from threading import Thread

from walking_agent import WalkingAgent


def main():
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger(__name__)

    # Set server uri of naoqi rpc server
    server_ip_address, server_port = '172.17.0.3', 8000
    server_uri = "http://{}:{}".format(server_ip_address, server_port)

    client = WalkingAgent(server_uri=server_uri)
    logger.info('Client started')

    logger.info('Move to (2, 0)')
    client.walk_to(2.0, 0, wait=True)
    logger.info('Finished')


if __name__ == '__main__':
    main()
