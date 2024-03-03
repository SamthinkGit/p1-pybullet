from utils.control import Analyzer, PID
from utils.pybullet_consts import CALIBRATION
from Fase4_bullet import main as fase4main
from icecream import ic
import pickle

def main():
    grad = I_GradientDescent(p=20.5, i=3.5, learning_rate=0.001)
    grad.start()
    try:
        while True:
            grad.step()
            print(f"Results: {grad.i_history[-1]}, {grad.score_history[-1]}")

    except KeyboardInterrupt:

        with open('dataset/slow_train.txt', 'wb') as f:
            pickle.dump((grad.i_history, grad.score_history), f)
        
        print("Training Interrupted")
        print(f"Values Reached: f{grad.i_history[-1], grad.score_history[-1]}")

class I_GradientDescent:

    def __init__(self, p: float, i:float, learning_rate: float) -> None:

        self.p = p
        self.i = i
        self.i_history = []
        self.score_history = []
        self.learning_rate = learning_rate

    def start(self):
        score1 = test_and_check(self.p, self.i)

        self.i_history.append(self.i)
        self.i_history.append(self.i + self.learning_rate)
        self.score_history.append(score1)

    #  /|
    # /_|
    #     x | (x2, y2) 
    # x     |
    # <----->
    # (x1, y1)
    # y2 - y1 / x2 - x1 -> Derivate 
        
    # x2 = input ahora
    # x1 = input antes
    # y1 = score antes
    # y2 = score ahora
        
    # d = score ahora - score antes / input ahora - input antes

    def step(self):

        ic(self.i_history, self.score_history)
        self.score_history.append(test_and_check(self.p, self.i_history[-1]))

        di = self.i_history[-1] - self.i_history[-2]
        if di == 0:
            di += self.learning_rate
        derivate = float((self.score_history[-1] - self.score_history[-2]) / di)
        new_i = self.i_history[-1] + derivate*self.learning_rate
        ic(derivate)
        ic(new_i)

        self.i_history.append(new_i)
        
def test_and_check(p, i):

    new_file = f"dataset/training_sample_{p}_{i}.csv"
    try:
        fase4main( 
            pid=PID(p,i,0.0,setpoint=2, shift=CALIBRATION.VEL_SHIFT),
            output_file=new_file,
            threading=True,
            maximum_time=4
        )
    except KeyboardInterrupt:
        raise
        
    except Exception:
        pass
    analyzer = Analyzer(set_real_values=True)
    analyzer.read_csv(new_file)
    score = analyzer.Y[0]
    
    return score

if __name__ == '__main__':
    main()