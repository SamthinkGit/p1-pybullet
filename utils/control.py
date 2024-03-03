from utils.pybullet_consts import CALIBRATION
from collections import deque
import numpy as np
import csv
import time

class PID:

    def __init__(self, Kp, Ki, Kd, setpoint, shift, umbral: float = CALIBRATION.UMBRAL):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.shift = shift
        self.setpoint = setpoint
        self.integral = 0
        self.previous_error = 0
        self.prev = None
        self.prev_output = 0
        self.umbral = umbral

    def start(self, start_value: float = 0):
        self.prev = time.perf_counter()
        self.update(start_value)

    #  /|
    # /_|
    #     x | (x2, y2) 
    # x     |
    # <----->
    # (x1, y1)
    # x2 - x1 / y2 - y1 -> Derivate 
        
    # x2 = momento ahora
    # x1 = momento antes
    # y2 = error ahora
    # y1 = error antes
        
    # d = error ahora - error antes / dt
        
    def update(self, measured_value):

        assert self.prev is not None, "[PID] Warning, pid.update() has been called without initializing. Use pid.start() first"

        now = time.perf_counter()
        dt = (now - self.prev)

        error = self.setpoint - measured_value
        self.integral = error * dt
        derivative = (error - self.previous_error) / dt
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative

        if abs(output) < self.umbral:
            output = 0

        self.prev = now
        self.previous_error = error
        self.prev_output = output


        return output + self.shift

class Analyzer:

    MAX_ERR = 10
    GOAL_POS = 19
    INVALID_SCORE = 100

    def __init__(self, set_real_values: bool = False) -> None:
        self._real_values = set_real_values

        self.X = []
        self.Y = []

    def read_csv(self, csv_name: str):
        # Reads a csv adding a new entry to the Analyzer
        # The output entry is: X+=[Kp, Ki, Kd], Y+=[score(Avg. error)]

        err = []
        with open(csv_name, 'r') as csvfile:

            reader = csv.DictReader(csvfile)
            assert 'err' in reader.fieldnames, "It looks the csv file points to a simulation without a PID"

            entry = next(reader)
            
            self.X.append([ float(entry[key]) for key in ['Kp', 'Ki', 'Kd', 'umbral'] ])
            err.append(float(entry['err']))

            goal_reached = False
            for row in reader:

                goal_reached = self._goal_reached(float(row['pos_x']))
                err.append(float(row['err']))
        
        if self._real_values or goal_reached:
            self.Y.append(self._score(err))
        else:
            self.Y.append(Analyzer.INVALID_SCORE)

    def _score(self, errors: list):
        if self._real_values:
            return np.mean(np.array(errors)**2)

        return min(np.mean(np.array(errors)**2), Analyzer.MAX_ERR)

    def _goal_reached(self, pos):
        return pos > Analyzer.GOAL_POS
            