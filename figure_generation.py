import matplotlib.pyplot as plt
import sys
import numpy as np
def read_dat(dat_file):
    tag_dict = {}
    with open(dat_file,'r') as f:
        for line in f:
            if line.startswith('v1 tag'):
                tag_info = line.split()
                tag_name = tag_info[2]
                tag_dict[tag_name] = {}
                tag_dict[tag_name]['color'] = tag_info[9]
                tag_dict[tag_name]['x'] = []
                tag_dict[tag_name]['y'] = []
            elif line.startswith('xp'):
                x_pos = int(float(line.split()[1]))
                tag_dict[tag_name]['x'].append(x_pos)
            elif line.startswith('yp'):
                y_pos = int(float(line.split()[1]))
                tag_dict[tag_name]['y'].append(y_pos)
    return tag_dict

def create_image(tag_dict):
    max_x = max([max(tag_dict[key]['x']) for key in tag_dict])
    max_y = max([max(tag_dict[key]['y']) for key in tag_dict])
    image = np.zeros((max_y+1, max_x+1, 3))
    for key in tag_dict:
        color = tag_dict[key]['color']
        r, g, b = [int(x) for x in color.split('(')[-1].split(')')[0].split(',')]
        x_list = tag_dict[key]['x']
        y_list = tag_dict[key]['y']
    for i in range(len(x_list)-1):
        start_x, end_x = x_list[i], x_list[i+1]
        start_y, end_y = y_list[i], y_list[i+1]
    if start_x == end_x and start_y == end_y:
        image[start_y][start_x] = [r/255, g/255, b/255]
    elif start_x == end_x:
        for y in range(min(start_y, end_y), max(start_y, end_y)+1):
            image[y][start_x] = [r/255, g/255, b/255]
    elif start_y == end_y:
        for x in range(min(start_x, end_x), max(start_x, end_x)+1):
            image[start_y][x] = [r/255, g/255, b/255]
    return image

def show_image(image):
    plt.imshow(image)
    plt.axis('off')
    plt.show()


dat_file = r'C:\Users\30389\AppData\Roaming\HypoMod\Model\Osmo\Graphs\gbase-Not found.dat'
tag_dict = read_dat(dat_file)
image = create_image(tag_dict)
show_image(image)
sys.path.append(r'C:\Users\30389\Desktop\system design\HypoModPython')
import subprocess
subprocess.run(["pdflatex", "-jobname=realosmo", r"C:\Users\30389\Desktop\system design\HypoModPython\Sheet1.tex"])

import matplotlib.pyplot as plt

time = [0, 300, 900, 1800]
vaso = [0.574, 4.32, 7.07, 11.57]

plt.plot(time, vaso, color='black')
plt.xlabel('Time')
plt.ylabel('Vaso')
plt.title('Vaso vs Time')
plt.show()