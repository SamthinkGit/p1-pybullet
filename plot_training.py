import pickle
import sys
from matplotlib import pyplot as plt
from pprint import pprint

if __name__ == '__main__':
    i = []
    score = []

    file = 'dataset/training_results_1.txt'
    file = 'dataset/training_results_2.txt'
    file = 'dataset/slow_train.txt'

    if len(sys.argv) > 1:
        file = sys.argv[1]

    with open(file=file, mode='rb') as f:
        i, score = pickle.load(f)

    for idx, row in enumerate(zip(i,score)):
        print(f"Iteration {idx}: {row}")
    fig, ax1 = plt.subplots()

    ax1.plot(score, 'g-', label="Score")
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Score', color='g')

    ax2 = ax1.twinx()
    ax2.plot(i[:-1], 'b-', label="I values")
    ax2.set_ylabel('I values', color='b')

    fig.tight_layout()
    plt.title('Training Results')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.show()

