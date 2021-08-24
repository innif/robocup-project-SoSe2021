import argparse
import math
from naoqi import ALProxy
from SimpleXMLRPCServer import SimpleXMLRPCServer


def main(robotIP, PORT=9559):
    rpc_server = SimpleXMLRPCServer(("0.0.0.0", 8000))

    rpc_server.register_introspection_functions()

    motionProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    def stand_init():
        # Send robot to Stand Init
        postureProxy.goToPosture("StandInit", 0.5)

    def setup_robot():
        # Wake up robot
        motionProxy.wakeUp()

        stand_init()

        #####################
        ## Enable arms control by move algorithm
        #####################
        motionProxy.setMoveArmsEnabled(True, True)

        motionProxy.moveInit()


    setup_robot()

    rpc_server.register_function(motionProxy.rest, 'rest')
    rpc_server.register_function(stand_init, 'stand_init')
    rpc_server.register_function(motionProxy.post.moveTo, 'moveTo')
    rpc_server.register_function(motionProxy.waitUntilMoveIsFinished, 'waitUntilMoveIsFinished')

    rpc_server.serve_forever()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--naoip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parser.add_argument("--naoport", type=int, default=9559,
                        help="Robot port number")

    args = parser.parse_args()
    main(args.naoip, args.naoport)
