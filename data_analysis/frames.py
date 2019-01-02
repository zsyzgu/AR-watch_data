import numpy as np
import pandas as pd
from pykalman import KalmanFilter
from point import Point

class Frames:
	timestamp = []
	acc = []
	gyr = []

	def __init__(self):
		self.timestamp = []
		self.acc = []
		self.gyr = []

	def len(self):
		n = len(self.timestamp)
		assert n == len(self.acc)
		assert n == len(self.gyr)
		return n

	def parseTime(self, str):
		tags = str.split('.')
		ms = int(tags[1])
		tags = tags[0].split(':')
		ms = ms + ((int(tags[0]) * 60 + int(tags[1])) * 60 + int(tags[2])) * 1000
		return ms

	def read_data(self, file):
		lines = open(file, 'r')
		for line in lines:
			tags = line.strip().split()
			if (len(tags) == 9):
				self.timestamp.append(self.parseTime(tags[0]))
				self.acc.append(Point(tags[3], tags[4], tags[5]))
				self.gyr.append(Point(tags[6], tags[7], tags[8]))
	
	def fix_timestamp(self):
		self.timestamp = np.array(self.timestamp) - self.timestamp[0]
		n = len(self.timestamp)
		j = 0
		for i in range(1, n):
			if (self.timestamp[i] != self.timestamp[i - 1]):
				self.timestamp[j : i] = np.linspace(self.timestamp[j], self.timestamp[i], i - j, endpoint = False)
				j = i

	def fix_acc(self):
		x, y, z = Point.points_2_xyz(self.acc)
		x -= np.median(x)
		y -= np.median(y)
		z -= np.median(z)
		self.acc = Point.xyz_2_points(x, y, z)

	def fix_gyr(self):
		x, y, z = Point.points_2_xyz(self.gyr)
		kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)

		self.gyr = Point.xyz_2_points(x, y, z)

	def caln_key_frame(self):
		A = [(self.gyr[i].x ** 2 + self.gyr[i].y ** 2 + self.gyr[i].z ** 2) ** 0.5 for i in range(len(self.gyr))]
		return A.index(max(A))

	def preprocess(self):
		self.fix_timestamp()
		self.fix_acc()
		self.fix_gyr()
