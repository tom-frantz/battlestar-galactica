import random


class Character(object):
	def __init__(self, **kwargs):
		self.name = random.choice()
		self.age = random.randint(18, 60)
		self.__dict__.update(kwargs)
