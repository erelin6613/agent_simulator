from simulator import BaseSimulator
from datetime import datetime
import time


# baseline time in miliseconds
TIME_BASELINE = 60*60*10
# time step to stay alive for leveling up
LEVEL_UP_STEP = 5*60
# maximum level of difficulty
MAX_LEVEL = 5

MAX_DEATHS = 5

HP = 100

class Agent:
	"""
	Assuming 5 levels of mastery the baseline would
	be equal to 3 updating based on the performance.
	"""
	def __init__(self, hp, init_time=None, level=MAX_LEVEL//2):
		self.hp = hp
		if init_time is None:
			self.init_time = int(time.time()*1000.0)
		self.level = level
		self.bad_luck = 0
		self.deaths = 0
		self.history = []

	def level_up(self):
		if self.level < MAX_LEVEL:
			self.level += 1

	def level_down(self):
		if self.bad_luck < 3:
			self.bad_luck = 0
			self.level -= 1
			self.deaths += 1
		else:
			self.bad_luck += 1

	def update(self):
		time = int(time.time()*1000.0) - self.init_time
		if time >= LEVEL_UP_STEP:
			self.level_up()
		params = {'time': time,
				'level': self.level,
				'deaths': self.death}
		self.log(params)

	def log(self, params):
		self.history.append(params)




