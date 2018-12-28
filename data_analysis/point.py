class Point:
	x = 0.0
	y = 0.0
	z = 0.0

	def __init__(self, *args):
		if (len(args) == 3):
			self.x = float(args[0])
			self.y = float(args[1])
			self.z = float(args[2])
		else:
			self.x = 0.0
			self.y = 0.0
			self.z = 0.0
	
	def __str__(self):
		return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'
