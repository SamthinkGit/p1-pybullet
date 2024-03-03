from utils import entities
from utils.pybullet_consts import PBConsts, CALIBRATION
from utils.templates import Husky
from utils.control import PID
from pprint import pprint

import pybullet as pb
import pybullet_data
import time
import logging

logging.basicConfig(level='DEBUG')

class Modules:

    def __init__(self, husky: Husky) -> None:
        self.husky = husky
        self.last_pos = 0
        self.safe_start = False

    def step(self):
            self.pos, _ = pb.getBasePositionAndOrientation(self.husky.info['id'])
    
    def save(self):
        # Each <DIST.FREQUENCY> save a register
        if self.pos[0] - self.last_pos > PBConsts.DISTANCE_FREQUENCY:
            self.last_pos = self.pos[0]
            self.husky.save()

    def step_pid(self):

            if self.safe_start and self.husky.info['pos']['x'] > CALIBRATION.SAFE_START_FOR_PID:
                logging.debug("[Modules] Safe-Start endpoint reached. Starting PID")
                self.husky.pid.start(start_value=self.husky.info['vel']['x'])
                self.safe_start = False
            
            if not self.safe_start:
                self.husky.auto_adjust()

    def enable_safe_start(self):
        self.safe_start = True

    def calibrate_vel(self, target_vel, accuracy):
        if round(self.husky.info['vel']['x'], accuracy) > round(target_vel, accuracy):
            self.husky.set_velocity_to(
                 vel=self.husky.input_vel[0] - (1./(10.**accuracy)),
                 forces=self.husky.forces
            )

        elif round(self.husky.info['vel']['x'], accuracy) < round(target_vel, accuracy):
            self.husky.set_velocity_to(
                 vel=self.husky.input_vel[0] + (1./(10.**accuracy)),
                 forces=self.husky.forces
            )
    
    def start_calibrated(self):
        self.husky.set_velocity_to(vel=CALIBRATION.VEL_SHIFT, forces=25)    # Requirement 3.1
        self.husky.set_dynamics(
            links=self.husky.wheels_idx,
            lateralFriction=0.93,
            spinningFriction=0.005,
            rollingFriction=0.003
        )                                           # Requirement 3.2

    def start_normal(self):
        self.husky.set_velocity_to(vel=13, forces=25)    # Requirement 3.1
        self.husky.set_dynamics(
            links=self.husky.wheels_idx,
            lateralFriction=0.93,
            spinningFriction=0.005,
            rollingFriction=0.003
        )                                           # Requirement 3.2

    def add_barriers(self, n_barriers: int = 1, start: float = 5):
        for i in range(n_barriers):
            barrier = pb.loadURDF(entities.get_sample_path("barrier.urdf"), useFixedBase=True)
            entities.aling_to_ground(barrier, x=start + 5*i, y=1.5)

        
def main():

    # Starting GUI
    client = pb.connect(pb.GUI)
    pb.setAdditionalSearchPath(pybullet_data.getDataPath())
    pb.setGravity(*PBConsts.GRAVITY)

    # Entities
    husky = pb.loadURDF("husky/husky.urdf")
    plane = pb.loadURDF("plane.urdf")

    # Building Husky
    husky = Husky(husky)
    modules = Modules(husky)
    L = 0.01
    T = 0.07
#    husky.set_pid(PID(1.2*(T/L), 2*L, 0.5*L, setpoint=2, shift=CALIBRATION.VEL_SHIFT))

    # Modules to prepare sandbox
    # modules.add_barriers(n_barriers=4, start=8)
    # modules.start_calibrated()
    modules.start_normal()
    modules.enable_safe_start()

    pb.setRealTimeSimulation(1)
    try:
        while True:

            husky.update()


            # Dynamic Modules:
            modules.step()
            modules.save()
            modules.calibrate_vel(target_vel=2, accuracy=2)
            #modules.step_pid()


            time.sleep(PBConsts.SLEEP_TIME)

    except KeyboardInterrupt as k:
        print("Interruption Received, Cleaning")


    print("Calibration results:")
    pprint(husky.input_vel)
    pprint(husky.forces)
    pprint(husky.info)

    # Save the history
    husky.to_csv(name='csv/sandbox_husky.csv')

    # Clean
    print("Program Stopped. Closing GUI")
    pb.disconnect()


if __name__ == '__main__':
    main()