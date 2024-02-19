from utils import entities
from utils.pybullet_consts import PBConsts
import pybullet as pb
import pybullet_data
import time

if __name__ == '__main__':

    # Starting GUI
    client = pb.connect(pb.GUI)
    pb.setAdditionalSearchPath(pybullet_data.getDataPath())
    pb.setGravity(*PBConsts.GRAVITY)

    # Entities
    plane = pb.loadURDF("plane.urdf")
#    husky = pb.loadURDF("husky/husky.urdf")
    ramp = pb.loadURDF(entities.get_sample_path("ramp.urdf"))

    entities.aling_to_ground(ramp)

    # Aligning
#    entities.aling_to_ground(item)

    # Running Simulation
    try:
        while True:

            pb.stepSimulation()
            time.sleep(PBConsts.CONTINOUS_FREQUENCY)


    except KeyboardInterrupt as k:

        print("Program Stopped. Closing GUI")
        pb.disconnect()