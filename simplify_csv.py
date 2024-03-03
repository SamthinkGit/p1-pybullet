from icecream import ic
import csv
import sys

if __name__ == '__main__':

    source = sys.argv[1]
    target = sys.argv[2]

    with open(source, 'r') as s:
        new_names = ['tiempo', 'posicion_robot', 'velocidad_ruedas', 'fuerza_ruedas']
        old_names = ['time', 'pos_x', 'vel_x', 'wheels_front_left_wheel_torque']

        reader = csv.DictReader(s)
        new_dict = [{new: row[old] for old, new in zip(old_names, new_names)} for row in reader]

    with open(target, 'w', newline='') as t:

        writer = csv.DictWriter(t,new_dict[0].keys())
        writer.writeheader()

        for row in new_dict:
            writer.writerow(row)
