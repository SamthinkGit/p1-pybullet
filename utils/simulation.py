import pybullet as pb
from threading import Event

stop_simulation_event = Event()

def simulation_signal_handler(sig, frame):
    # Used for avoiding active waiting

    print("Program Stopped. Closing GUI")
    pb.disconnect()
    stop_simulation_event.set()