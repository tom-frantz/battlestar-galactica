import math


def pythagoras(a, b):
	return math.sqrt((a ** 2) + (b ** 2))


class FleetHandler(object):
	def __init__(self):
		self.fleets = []

	def generate_colonial_fleet(self, default=True):
		fleet = Fleet()
		if default:
			fleet.ships.append(Ship(0, 'Battlestar Galactica', 25000000, 3, subsystems=[
				SubSystem('Bridge', 'command', {'manoeuvre': 10, 'warp_timer': 15, 'planning': 10, 'organisation': 10, 'skill_bonus': 10})
			]))
		self.fleets.append(fleet)


class Fleet(object):
	def __init__(self):
		self.ships = []


class Ship(object):
	def __init__(self, id, name, mass, acceleration, **kwargs):
		self.id = id
		self.name = name
		self.subsystems = []
		self.mass = mass
		self.acceleration = acceleration


class SubSystem(object):
	def __init__(self, name, type, stats):
		self.name = name
		self.type = type
		self.stats = stats
