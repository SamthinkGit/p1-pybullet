import matplotlib.pyplot as plt
import csv

if __name__ == '__main__':

    csv_file = 'husky_info.csv'
    x, y = [], []

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x.append(float(row['pos_x']))
            y.append(float(row['vel_x']))

    plt.plot(x, y, linestyle='-', color='b')
    plt.title(f'Husky Speed vs Position')
    plt.xlabel("Position Axis-X (m)")
    plt.ylabel("Velocity (m/s)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()