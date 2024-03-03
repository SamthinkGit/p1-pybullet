from utils import entities
from utils.pybullet_consts import PBConsts, CALIBRATION
from utils.templates import Husky
from utils.control import PID
from sandbox import Modules

from icecream import ic

import argparse
import pybullet as pb
import pybullet_utils.bullet_client as bc
import pybullet_data
import time

def main(
        # Parameters only for training
        pid: PID = None,
        output_file=None,
        threading: bool = False,
        maximum_time: float = 16,
    ):

    # Parsing optional arguments
    parser = argparse.ArgumentParser(description='Runs a simulation of the husky driving through a barrier')
    parser.add_argument('--csv', type=str, help='Select the name for the output csv file.', default='Fase4.csv')
    args = parser.parse_args()

    # Starting GUI

    client = pb.connect(pb.GUI)
    pb.setAdditionalSearchPath(pybullet_data.getDataPath())
    pb.setGravity(*PBConsts.GRAVITY)


    # Entities
    husky = pb.loadURDF("husky/husky.urdf")
    plane = pb.loadURDF("plane.urdf")
    ramp = pb.loadURDF(entities.get_sample_path("ramp.urdf"))
    barrier = pb.loadURDF(entities.get_sample_path("barrier.urdf"), useFixedBase=True)
    goal = pb.loadURDF(entities.get_sample_path("goal.urdf"))

    entities.aling_to_ground(ramp, x=10)
    entities.aling_to_ground(barrier)
    entities.aling_to_ground(barrier, x=17, y=1.5, shift=-0.4)
    entities.aling_to_ground(goal, x=20)


    # Building Husky
    husky = Husky(husky)
    modules = Modules(husky)
    modules.start_calibrated()
    modules.enable_safe_start()

    if threading:
        husky.set_pid(pid) # Training PID
    else:
        husky.set_pid(PID( 20.5, 3.6, 0.0 , setpoint=2, shift=CALIBRATION.VEL_SHIFT))

    # Requirement 3.3
    stick = entities.find_joint_idx('base2stick', barrier)
    pb.changeDynamics(barrier, stick, localInertiaDiagonal=[0.41]*3)

    # Running Simulation
    if not threading:
        pb.setRealTimeSimulation(1)

    # Some training params
    start = time.perf_counter()
    last_pos = 0

    try:
        while True:
            
            # Stopping Simulation if goal is not reachable (Training)
            current_time = time.perf_counter()
            if threading and current_time - start > maximum_time:
                break

            pos, _ = pb.getBasePositionAndOrientation(husky.info['id'])
            if pos[0] >= 20 or pos[0] < last_pos: 
                break

            # Running modules
            modules.step()
            modules.save()
            modules.step_pid()

            # Update husky status + PID
            husky.update()
            
            # Step or sleep (Depending if it is training)
            if threading:
                pb.stepSimulation()
            else:
                time.sleep(PBConsts.SLEEP_TIME)

    except KeyboardInterrupt as k:
        print("Interruption Received, Cleaning")

    # Save the history
    if not threading:
        husky.to_csv(name=f"csv/{args.csv}")
    else:
        husky.to_csv(name=output_file)

    # Clean
    print("Program Stopped. Closing GUI")
    pb.disconnect()


if __name__ == '__main__':
    main()
