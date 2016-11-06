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
			SubSystem(0, 'Bridge', 'command/navigation', {'manoeuvre': 10, 'warp_timer': 15, 'planning': 10, 'organisation': 10, 'skill_bonus': 10}),
			SubSystem(1, 'Ion Engines', 'propulsion', {'thrust_max': 3, 'thrust_average': 0.5, 'manoeuvre': 10, 'base_fuel_consumption': 1}),
			SubSystem(2, 'Tylium Tanks', 'fuel_storage', {'fuel_max': 50, 'fuel_current': 10, 'fuel_type': 'civilian_distilled'}),
			SubSystem(3, 'Commander\'s Quarters', 'cabin', {'cabin_max': 5, 'cabin_current': 5, 'quality': 14, 'type': 'commander\'s_cabin', 'cabins': 5}),
			SubSystem(4, 'Officer\'s Cabins', 'cabin', {}),
			SubSystem(5, 'Pilot Cabins', 'cabin', {}),
			SubSystem(6, 'Marine Bunks', 'cabin', {}),
			SubSystem(7, 'Enlisted Cabins', 'cabin', {}),
			SubSystem(8, 'Fusion Generators', 'power_generator', {}),
			SubSystem(9, 'Life Support Generators', 'life_support', {}),
			SubSystem(10, 'DRADIS', 'spacial_sensor', {}),
			SubSystem(11, 'Neutrino Sensor', 'radiation_sensor', {}),
			SubSystem(12, 'Jammer', 'signal_jammer', {}),
			SubSystem(13, 'Heavy Kinetic Turrets', 'weapon', {}),
			SubSystem(14, 'Point Defense Mounts', 'weapon', {}),
			SubSystem(15, 'Flight Pods', 'hanger', {}),
			SubSystem(16, 'Launch Tubes', 'launch_system', {}),
			SubSystem(17, 'Engineering Bay', 'engineering_bay', {}),
			SubSystem(18, 'Research Lab', 'research_lab', {}),
			SubSystem(19, 'Logistics Hub', 'logistics_hub', {}),
			SubSystem(20, 'Computer Lab', 'computer_lab', {}),
			SubSystem(21, 'Pilot\'s Breifing Room', 'pilot_briefing_room', {}),
			SubSystem(22, 'Brig', 'prison', {}),
			SubSystem(23, 'Colonial Chapel', 'religious_room', {}),
			SubSystem(24, 'Recreational Facilities', 'recreational_room', {}),
			SubSystem(25, 'Courtroom', 'court', {}),
			SubSystem(26, 'Cargo Hold', 'cargo_bay', {})
		]))
		self.fleets.append(fleet)


class Fleet(object):
	def __init__(self):
		self.ships = []


class Ship(object):
	def __init__(self, ID, name, mass, acceleration, **kwargs):
		self.id = ID
		self.name = name

		self.crew = 2700
		self.crew_max = 5040

		self.mass = mass
		self.acceleration = acceleration
		self.acceleration_current = 0

		self.stats = {}
		self.subsystems = []

		self.__dict__.update(kwargs)


class SubSystem(object):
	def __init__(self, number, name, type, stats):
		self.id = number
		self.type = type
		self.name = name
		self.stats = stats
