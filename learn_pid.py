from utils.control import Analyzer
from Fase4_bullet import main as fase4main
from utils.pybullet_consts import CALIBRATION

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from utils.control import PID
from matplotlib import pyplot as plt
import numpy as np
import os
import sys
import time

TRAIN = True
PLOT = True 

def main():


    if TRAIN:
        build_dataset()

    if not PLOT:
        return

    analyzer = Analyzer()
    mode = sys.argv[1]
    for file in os.listdir('dataset'):
        if file.startswith(mode):
            analyzer.read_csv(f"dataset/{file}")

    analyzer.Y, analyzer.X = zip(*sorted(zip(analyzer.Y, analyzer.X)))

    stop_val = 0
    for idx, val in enumerate(analyzer.Y):
        if val > 3:
            stop_val = idx
            break
            

    top_x = analyzer.X[:stop_val]
    top_y = analyzer.Y[:stop_val]
    if PLOT:
        p, i, d, _ = zip(*top_x)

        plt.scatter(p, top_y)
        plt.xlabel('PID valeus')
        plt.ylabel('Score')
        plt.title('P training')
        plt.show()

        plt.scatter(i, top_y)
        plt.xlabel('PID valeus')
        plt.ylabel('Score')
        plt.title('I training')
        plt.show()

#        plt.scatter(d, top_y)
#        plt.xlabel('PID valeus')
#        plt.ylabel('Score')
#        plt.title('D training')
#        plt.show()


def build_dataset():

    # 4*30*20
#    for p in np.arange(19,22,0.1):
#        for i in np.arange(3, 5, 0.1):

    for p in np.arange(0.0,35.0,0.5):
        for i in np.arange(3.4, 3.5, 0.5):

            new_file = f"dataset/big_samples_{p}_{i}.csv"

            if Path(new_file).exists():
                print(f"Dataset {new_file} already computed, skipping")
                continue

            try:
                fase4main( 
                    pid=PID(p,i,0.0,setpoint=2, shift=CALIBRATION.VEL_SHIFT),
                    output_file=new_file,
                    threading=True,
                    maximum_time=4
                )
            except Exception:
                pass


if __name__ == '__main__':
    main()
