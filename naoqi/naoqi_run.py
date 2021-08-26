import argparse
import base64
from SimpleXMLRPCServer import SimpleXMLRPCServer

import qi


class NaoqiRunner():

    def __init__(self, robot_ip, port=9559):
        self.rpc_server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
        self.session = qi.Session()
        self.session.connect("tcp://" + robot_ip + ":" + str(port))

        self.motion_proxy  = self.session.service("ALMotion")
        self.posture_proxy = self.session.service("ALRobotPosture")
        self.cam_proxy = self.session.service("ALVideoDevice")

        self.rpc_server.register_introspection_functions()

        self._register_functions()

    def _register_functions(self):
        self.rpc_server.register_function(self.motion_proxy.rest, 'rest')
        self.rpc_server.register_function(self.stand_init, 'stand_init')
        self.rpc_server.register_function(self.motion_proxy.moveTo, 'moveTo')
        self.rpc_server.register_function(self.motion_proxy.waitUntilMoveIsFinished, 'waitUntilMoveIsFinished')

        self.rpc_server.register_function(self.subscribe_to_cam, 'subscribe_to_cam')
        self.rpc_server.register_function(self.unsubscribe_from_cam, 'unsubscribe_from_cam')
        self.rpc_server.register_function(self.get_image, 'get_image')

        self._video_client = None

    def subscribe_to_cam(self, resolution, color_space):
        self._video_client = self.cam_proxy.subscribe("python_client", resolution, color_space, 5)

    def unsubscribe_from_cam(self):
        if not self._video_client:
            raise ValueError('Camera has not been subscribed to yet')

        self.cam_proxy.unsubscribe(self._video_client)

    def get_image(self):
        # if not self._video_client:
        #     raise ValueError('Camera has not been subscribed to yet')

        image = self.cam_proxy.getImageRemote(self._video_client)
        encoded_image = image[:6]
        encoded_image.append(base64.b64encode(image[6]))
        return encoded_image

    def stand_init(self):
        # Send robot to Stand Init
        self.posture_proxy.goToPosture("StandInit", 0.5)

    def setup_robot(self):
        # Wake up robot
        self.motion_proxy.wakeUp()

        self.stand_init()

        #####################
        ## Enable arms control by move algorithm
        #####################
        self.motion_proxy.setMoveArmsEnabled(True, True)

        self.motion_proxy.moveInit()

    def main(self):
        self.setup_robot()

        self.rpc_server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--naoip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--naoport", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    runner = NaoqiRunner(args.naoip, args.naoport)
    runner.main()
