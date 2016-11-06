import math


def pythagoras(a, b):
	return math.sqrt((a ** 2) + (b ** 2))


class FleetHandler(object):
	def __init__(self):
		self.unassigned = []
		self.fleets = []

	def generate_colonial_fleet(self):
		fleet = Fleet()
		fleet.ships.append(Ship(0, 'Battlestar Galactica', 25000000, 3, subsystems=[
			SubSystem(0, 'Bridge', {'manoeuvre': 10, 'warp_timer': 15, 'planning': 10, 'organisation': 10, 'skill_bonus': 10}),
			SubSystem(1, )
		]))
		self.fleets.append(fleet)


class Fleet(object):
	def __init__(self):
		self.ships = []


class Ship(object):
	def __init__(self, ID, name, mass, acceleration, **kwargs):
		self.id = ID
		self.name = name
		self.mass = mass
		self.acceleration = acceleration
		self.stats = {}
		self.subsystems = []

		self.__dict__.update(kwargs)


class SubSystem(object):
	def __init__(self, ID, name, stats):
		self.id = ID
		self.name = name
		self.stats = stats
