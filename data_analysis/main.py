import os
import sys
from matplotlib import pyplot as plt
import math
import numpy as np

class DataFrame:
	type = ''
	timestamp = 0.0
	x = 0.0
	y = 0.0
	z = 0.0

def get_file_list():        
	root_dir = '.'
	file_name = os.listdir(root_dir)

	file_list = []
	for i in range(0, len(file_name)):
		path = os.path.join(root_dir, file_name[i])
		if os.path.isfile(path) and path.split('.')[-1] == 'log':
			file_list.append(path)

	return file_list

def read_data(file):
	acc_list = []
	gyr_list = []

	lines = open(file, 'r')
	for line in lines:
		tags = line.strip().split(', ')
		if (len(tags) == 5):
			frame = DataFrame()
			frame.type = tags[0]
			frame.timestamp = float(tags[1])
			frame.x = float(tags[2])
			frame.y = float(tags[3])
			frame.z = float(tags[4])
			if frame.type == 'Acc':
				acc_list.append(frame)
			else:
				gyr_list.append(frame)
	
	return acc_list, gyr_list

def analyze_data(file):
	acc_list, gyr_list = read_data(file)
	
	plt.figure(file)

	acc_t = [acc_list[i].timestamp for i in range(len(acc_list))]
	acc_x = [acc_list[i].x for i in range(len(acc_list))]
	acc_y = [acc_list[i].y for i in range(len(acc_list))]
	acc_z = [acc_list[i].z for i in range(len(acc_list))]
	acc_t = np.array(acc_t) - acc_t[0]
	acc_x = acc_x - np.mean(acc_x)
	acc_y = acc_y - np.mean(acc_y)
	acc_z = acc_z - np.mean(acc_z)
	plt.subplot(2, 1, 1)
	plt.title('Acc')
	plt.plot(acc_t, acc_x, acc_t, acc_y, acc_t, acc_z)
	
	gyr_t = [gyr_list[i].timestamp for i in range(len(gyr_list))]
	gyr_x = [gyr_list[i].x for i in range(len(gyr_list))]
	gyr_y = [gyr_list[i].y for i in range(len(gyr_list))]
	gyr_z = [gyr_list[i].z for i in range(len(gyr_list))]
	gyr_t = np.array(gyr_t) - gyr_t[0]
	gyr_x = gyr_x - np.mean(gyr_x)
	gyr_y = gyr_y - np.mean(gyr_y)
	gyr_z = gyr_z - np.mean(gyr_z)
	plt.subplot(2, 1, 2)
	plt.title('Gyr')
	plt.plot(gyr_t, gyr_x, gyr_t, gyr_y, gyr_t, gyr_z)

	plt.show()

file_list = get_file_list()
for file in file_list:
	analyze_data(file)
