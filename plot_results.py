import matplotlib.pyplot as plt
import argparse
import csv

def plot_husky_data(csv_file: str, color: str, label: str, use_pid: bool=True) -> None:

    x, y1, y2, y3 = [], [], [], []

    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x.append(float(row['pos_x']))
            y1.append(float(row['vel_x']))
            if use_pid:
                pid = row.get('pid_out')
                y2.append(float(pid) if pid else 0)

    plt.plot(x, y1, linestyle='-', color=color, label=label)
    if use_pid:
        plt.plot(x, y2, linestyle='-.', color='k', label=f"PID output")

if __name__ == '__main__':

    # Arguments 
    parser = argparse.ArgumentParser(description='Plots a husky simulation graph. It will plot velocity vs position')
    parser.add_argument('--select', type=str, help='Select a csv file for plotting. Use all for combine all plots', default='all')
    parser.add_argument('--adjust', type=str, help='Select the position of the legend', default='lower right')
    parser.add_argument('--pid', type=bool, help='Show PID behavior', default=False)
    args = parser.parse_args()

    match args.select:
        case 'compare':
            csv_files = [f"./csv/Fase{version}.csv"  for version in [3.3, 4]]
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
        ['Ascent', 5.0],
        ['Peak', 8.0],
        ['Descent', 12.0],
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
        plot_husky_data(file, color=line_colors[idx], label=file, use_pid=args.pid)

    # Coloring background
    for idx, (name, val) in enumerate(key_points[:-1]):
        plt.axvspan(val, key_points[idx+1][1], color=colors[idx], alpha=0.1, label=name)

    # Some enhancements
    plt.title(f'Husky Speed vs Position')
    plt.xlabel("Position Axis-X (m)")
    plt.ylabel("Velocity (m/s)")
    plt.tight_layout(rect=[0,0,2,0])
    plt.legend(loc=args.adjust, ncol=2).get_frame().set_alpha(0.9)
    plt.grid(True, alpha=0.2)

    try:
        plt.show()
    except KeyboardInterrupt:
        print("Closing")
        plt.close()