import argparse
from naoqi import ALProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer


class NaoqiRunner():

    def __init__(self, robot_ip, port=9559):
        self.rpc_server = SimpleXMLRPCServer(("0.0.0.0", 8000))

        self.motionProxy  = ALProxy("ALMotion", robot_ip, port)
        self.postureProxy = ALProxy("ALRobotPosture", robot_ip, port)

        self.rpc_server.register_introspection_functions()


        self.rpc_server.register_function(self.motionProxy.rest, 'rest')
        self.rpc_server.register_function(self.stand_init, 'stand_init')
        self.rpc_server.register_function(self.motionProxy.post.moveTo, 'moveTo')
        self.rpc_server.register_function(self.motionProxy.waitUntilMoveIsFinished, 'waitUntilMoveIsFinished')


    def stand_init(self):
        # Send robot to Stand Init
        self.postureProxy.goToPosture("StandInit", 0.5)

    def setup_robot(self):
        # Wake up robot
        self.motionProxy.wakeUp()

        self.stand_init()

        #####################
        ## Enable arms control by move algorithm
        #####################
        self.motionProxy.setMoveArmsEnabled(True, True)

        self.motionProxy.moveInit()

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
