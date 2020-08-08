from simulators import BaseSimulator
from datetime import datetime
import time
import numpy as np

# baseline time in miliseconds
TIME_BASELINE = 10
# time step to stay alive for leveling up
LEVEL_UP_STEP = 5
# maximum level of difficulty
MAX_LEVEL = 5

MAX_DEATHS = 5

HP = 100

DAMAGE = 1

class Agent:
	"""
	Assuming 5 levels of mastery the baseline would
	be equal to 2 updating based on the performance.
	"""
	def __init__(self, hp, init_time=None, level=MAX_LEVEL//2):
		self.hp = hp
		if init_time is None:
			self.init_time = time.time_ns()
		self.level = level
		self.bad_luck = 0
		self.deaths = 0
		self.history = []
		self.damage_count = 0

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
		t = time.time_ns() - self.init_time
		#print(t/1e9, TIME_BASELINE)
		if t >= LEVEL_UP_STEP/1e9 and t > TIME_BASELINE*1e9:
			self.level_up()

		params = {'time': round(t/1e9, 3),
				'level': self.level,
				'hp': self.hp,
				'deaths': self.deaths,
				'damage recived': self.damage_count*DAMAGE}
		#print(t+self.init_time, TIME_BASELINE*1e9)
		self.log(params)

	def log(self, params):
		self.history.append(params)
		self.history = list(
			{item['time']: item for item in self.history}.values())


class Enemy:

	def __init__(self):
		"""
		what metrics of enemies will be adjusted? Those are
		purely my suggestions

		self.speed = speed
		self.misses = misses
		"""
		pass

	def update(self):
		"""
		self.speed -= speed step
		self.misses += miss_ptc
		"""
		pass


class GameSimulator(BaseSimulator):

	def __init__(self, agent, enemy):
		super().__init__(trials=1)
		self.agent = agent
	
	def process_function(self):
		"""Debug is not finished yet! Problem:
		damage count exceeds the maximum"""
		while self.agent.deaths < MAX_DEATHS:
			# assuming each milliseconds we will update the status
			time.sleep(0.001)
			# probability getting DAMAGE pt of damage - 20% for now
			# ideally it comes from environment i.e. game
			# 0 - no damage, DAMAGE otherwise
			c = self.get_choice(choices=[0, DAMAGE], p=[0.8, 0.2])
			if c != 0:
				self.agent.hp -= c
				self.agent.damage_count += 1
				#print(self.agent.hp, self.agent.damage_count, self.agent.deaths)
			if self.agent.hp < 1:
				stay_alive = self.get_choice(p=[0.5, 0.5])
				if stay_alive == 0:
					self.agent.deaths += 1
				self.agent.hp = HP
			self.agent.update()
		print(self.agent.history[-1])


	def get_choice(self, choices=[0, 1], p=[0.7, 0.3]):
		"""
		Random number generator.
		"""
		choice = np.random.choice(choices, p=p, size=1)
		return choice[0]


if __name__ == '__main__':
	agent = Agent(HP)
	enemy = Enemy()
	simulator = GameSimulator(agent, enemy)
	simulator.run_trials()