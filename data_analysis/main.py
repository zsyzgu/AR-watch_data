import os
import sys
from matplotlib import pyplot as plt
import math
import numpy as np
import pandas as pd

from point import Point

class DataFrame:
	timestamp = 0.0
	acc = Point()
	gyr = Point()

def get_file_list():
	root_dir = '.'
	file_name = os.listdir(root_dir)

	file_list = []
	for i in range(0, len(file_name)):
		path = os.path.join(root_dir, file_name[i])
		if os.path.isfile(path) and path.split('.')[-1] == 'log':
			file_list.append(path)

	return file_list

def parseTime(str):
	tags = str.split('.')
	ms = int(tags[1])
	tags = tags[0].split(':')
	ms = ms + ((int(tags[0]) * 60 + int(tags[1])) * 60 + int(tags[2])) * 1000
	return ms

def read_data(file):
	frames = []

	lines = open(file, 'r')
	for line in lines:
		tags = line.strip().split()
		if (len(tags) == 9):
			frame = DataFrame()
			frame.timestamp = parseTime(tags[0])
			frame.acc = Point(tags[3], tags[4], tags[5])
			frame.gyr = Point(tags[6], tags[7], tags[8])
			frames.append(frame)
	
	return frames

def fix_timestamp(timestamp):
	n = len(timestamp)
	j = 0
	for i in range(1, n):
		if (timestamp[i] != timestamp[i - 1]):
			timestamp[j : i] = np.linspace(timestamp[j], timestamp[i], i - j, endpoint = False)
			j = i
	print timestamp
	return timestamp

def fix_acc(acc):
	# acc = pd.Series(acc)
	# acc_mean = acc.rolling(window = 20).mean()
	# TODO
	pass

def draw_points(timestamp, points):
	n = len(timestamp)
	assert n == len(points)
	x = [points[i].x for i in range(n)]
	y = [points[i].y for i in range(n)]
	z = [points[i].z for i in range(n)]
	plt.plot(timestamp, x, timestamp, y, timestamp, z)

def draw_frames(frames):
	n = len(frames)
	timestamp = [frames[i].timestamp for i in range(n)]
	timestamp = np.array(timestamp) - timestamp[0]
	timestamp = fix_timestamp(timestamp)
	acc = [frames[i].acc for i in range(n)]
	gyr = [frames[i].gyr for i in range(n)]
	
	plt.figure(file)

	plt.subplot(2, 1, 1)
	plt.title('acc')
	draw_points(timestamp, acc)

	plt.subplot(2, 1, 2)
	plt.title('gyr')
	draw_points(timestamp, gyr)

	plt.show()

if __name__ == '__main__':
	file_list = get_file_list()
	for file in file_list:
		frames = read_data(file)
		draw_frames(frames)
