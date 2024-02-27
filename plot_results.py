import matplotlib.pyplot as plt
import argparse
import csv

def plot_husky_data(csv_file: str, color: str, label: str) -> None:

    x, y = [], []

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x.append(float(row['pos_x']))
            y.append(float(row['vel_x']))

    plt.plot(x, y, linestyle='-', color=color, label=label)


if __name__ == '__main__':

    # Arguments 
    parser = argparse.ArgumentParser(description='Plots a husky simulation graph. It will plot velocity vs position')
    parser.add_argument('--select', type=str, help='Select a csv file for plotting. Use all for combine all plots', default='all')
    args = parser.parse_args()

    match args.select:
        case 'all':
            csv_files = [f"./csv/Fase{version}.csv"  for version in [3.1, 3.2, 3.3]]
        case _:
            csv_files = [args.select]

    # Declarations
    husky_shift = 0.3
    key_points = [
        # Note: These are only aproximations, is 
        # not fully considering husky size 
        ['Start', 0.0],
        ['Ramp Ascent', 5.0],
        ['Ramp Peak', 8.0],
        ['Ramp Descent', 12.0],
        ['Floor', 15.0],
        ['Barrier', 17.0],
        ['End', 20.0],
    ]
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    line_colors = ['r','g','b']


    for point in key_points: 
        point[1] -= husky_shift
    
    # Plotting CSV
    for idx, file in enumerate(csv_files):
        plot_husky_data(file, color=line_colors[idx], label=file)

    # Coloring background
    for idx, (name, val) in enumerate(key_points[:-1]):
        plt.axvspan(val, key_points[idx+1][1], color=colors[idx], alpha=0.1, label=name)

    # Some enhancements
    plt.title(f'Husky Speed vs Position')
    plt.xlabel("Position Axis-X (m)")
    plt.ylabel("Velocity (m/s)")
    plt.tight_layout()
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.2)

    try:
        plt.show()
    except KeyboardInterrupt:
        print("Closing")
        plt.close()