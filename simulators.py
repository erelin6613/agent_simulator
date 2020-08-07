import numpy as np
from tqdm import tqdm
import time

class BaseSimulator:
	"""
	An abstract class representing a :class:`BaseSimulator`.

	The BaseSilulator is used to build custom simulators.
	The defenition and methods in this class are serving
	more as a utilities that will help to built simulators
	easier such as running trials, logging results of 
	simulations, etc. 			
	"""

	def __init__(self, trials=1e5, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		self.trails=int(trials)

	def __repr__(self):
		return self.__name__

	def __str__(self):
		return self.name

	def process_function(self):
		"""
		Method in BaseSimulator meant to be overwritten
		to a specific simulator functions.
		```
			class MySimulator(BaseSimulator):
				def __init__(self):
					super().__init__()

				def process_function(self, x):
					import time
					time.sleep(x)
	 	```
	 	"""
		pass

	def get_object(self, obj):
		return obj

	def run_trials(self, log_counts=True, *args, **kwargs):
		"""
		Runs of trials (specified by process_function), the
		number of trials specified as property self.trials.

		:param: log_count(bool) - wheather to log metrics and
					return them as a result of the method.
		:return: dictionary if log_counts is True.
		"""

		print('Running {} simulations ...'.format(self.trials))
		if log_counts:
			counts = {}
		for i in tqdm(range(self.trials)):
			if log_counts:
				counts = self.process_function()
			else:
				self.process_function()
		print('Ran {} simulations'.format(self.trials))
		if log_counts:
			return counts

	def log_counts(self, counts, exclude=None):
		"""
		Increament metrics after trial is performed, both
		expects and returns dictionary of metrics. If
		some metrics should not be increamented, those
		should be specidied in a list and passed to the
		method as `exclude` parameter.
		"""

		for k in counts.keys():
			if k in exclude:
				continue
			counts[k] += 1
		return counts

	def explain(self):
		return'This function explains some key points about your simulator.\
			Feel free to overwrite it to explain when developing a\
			custom simulator.'
