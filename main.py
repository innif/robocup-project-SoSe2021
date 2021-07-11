import logging
from threading import Thread
from time import sleep

from robolib import ServerAgent
from walking_agent import WalkingAgent


def main():
    logging.getLogger().setLevel(logging.INFO)

    logger = logging.getLogger(__name__)

    server_ip_address, server_port = 'localhost', 8888
    server_uri = f"http://{server_ip_address}:{server_port}"

    server = ServerAgent(ip_address=server_ip_address, port=server_port)
    server_thread = Thread(target=server.run)
    server_thread.start()
    logger.info('Server started')

    client = WalkingAgent(server_uri=server_uri)
    logger.info('Client started')
    sleep(2)

    client.dance()


if __name__ == '__main__':
    main()