import os
import sys
from matplotlib import pyplot as plt
import math
import numpy as np
import pandas as pd
from point import Point
from frames import Frames

def get_file_list():
	root_dir = '.'
	file_name = os.listdir(root_dir)

	file_list = []
	for i in range(0, len(file_name)):
		path = os.path.join(root_dir, file_name[i])
		if os.path.isfile(path) and path.split('.')[-1] == 'log':
			file_list.append(path)

	return file_list

def draw_points(timestamp, points):
	n = len(timestamp)
	assert n == len(points)
	x, y, z = Point.points_2_xyz(points)
	plt.plot(timestamp, x, timestamp, y, timestamp, z)

def draw_frames(frames):
	timestamp = frames.timestamp
	acc = frames.acc
	gyr = frames.gyr
	key_gyr = frames.caln_key_frame()

	plt.figure(file)

	plt.subplot(2, 1, 1)
	plt.title('acc')
	draw_points(timestamp, acc)

	plt.subplot(2, 1, 2)
	plt.title('gyr')
	draw_points(timestamp, gyr)
	plt.axvline(timestamp[key_gyr], color = 'red')
	plt.axvline(timestamp[key_gyr - 100], color = 'green')
	plt.axvline(timestamp[key_gyr + 100], color = 'green')

	plt.show()

if __name__ == '__main__':
	file_list = get_file_list()
	for file in file_list:
		frames = Frames()
		frames.read_data(file)
		frames.preprocess()
		draw_frames(frames)

