import math


class FleetHandler(object):
	def __init__(self):
		self.unassigned = []
		self.fleets = []

	def generate_battlestar(self, **kwargs):
		fleet = Fleet([0, 0], 'Caprica', primary_fleet=True)
		fleet.ships.append(Ship(0, 'Battlestar Galactica', 2700, 5040, 25000000, 3, subsystems=[
			SubSystem(0, 'Bridge', 'command/navigation', {'manoeuvre': 10, 'warp_timer': 15, 'planning': 10, 'organisation': 10, 'skill_bonus': 10}),
			SubSystem(1, 'Ion Engines', 'propulsion', {'thrust_max': 3, 'thrust_average': 0.5, 'manoeuvre': 10, 'base_fuel_consumption': 1}),
			SubSystem(2, 'FTL', 'faster_than_light', {}),
			SubSystem(3, 'Tylium Tanks', 'fuel_storage', {'fuel_max': 50, 'fuel_current': 10, 'fuel_type': 'civilian_distilled'}),
			SubSystem(4, 'Commander\'s Quarters', 'cabin', {'cabin_max': 5, 'cabin_current': 5, 'quality': 14, 'type': 'commander\'s_cabin', 'cabins': 5}),
			SubSystem(5, 'Officer\'s Cabins', 'cabin', {}),
			SubSystem(6, 'Pilot Cabins', 'cabin', {}),
			SubSystem(7, 'Marine Bunks', 'cabin', {}),
			SubSystem(8, 'Enlisted Cabins', 'cabin', {}),
			SubSystem(9, 'Fusion Generators', 'power_generator', {}),
			SubSystem(10, 'Life Support Generators', 'life_support', {}),
			SubSystem(11, 'DRADIS', 'spacial_sensor', {}),
			SubSystem(12, 'Neutrino Sensor', 'radiation_sensor', {}),
			SubSystem(13, 'Jammer', 'signal_jammer', {}),
			SubSystem(14, 'Heavy Kinetic Turrets', 'weapon', {}),
			SubSystem(15, 'Point Defense Mounts', 'weapon', {}),
			SubSystem(16, 'Flight Pods', 'hanger', {}),
			SubSystem(17, 'Launch Tubes', 'launch_system', {}),
			SubSystem(18, 'Engineering Bay', 'engineering_bay', {}),
			SubSystem(19, 'Research Lab', 'research_lab', {}),
			SubSystem(20, 'Logistics Hub', 'logistics_hub', {}),
			SubSystem(21, 'Computer Lab', 'computer_lab', {}),
			SubSystem(22, 'Pilot\'s Breifing Room', 'pilot_briefing_room', {}),
			SubSystem(23, 'Brig', 'prison', {}),
			SubSystem(24, 'Hospital', 'medical', {}),
			SubSystem(25, 'Colonial Chapel', 'religious_room', {}),
			SubSystem(26, 'Recreational Facilities', 'recreational_room', {}),
			SubSystem(27, 'Courtroom', 'court', {}),
			SubSystem(28, 'Cargo Hold', 'cargo_bay', {})
		]))
		self.fleets.insert(0, fleet)
		self.__dict__.update(kwargs)


class Fleet(object):
	def __init__(self, global_location, orbit_location, **kwargs):
		self.primary_fleet = False
		self.ships = []
		# global_location = [x coord, y coord]
		self.global_location = global_location
		self.orbit = {
			'orbit_body': orbit_location,
			# 'orbit_type's: 'circular', 'eccentric', 'collision course'
			'orbit_type': 'stable'
		}

		self.__dict__.update(kwargs)


class Ship(object):
	def __init__(self, ID, name, crew, crew_max, mass, acceleration, **kwargs):
		self.id = ID
		self.name = name

		self.crew = crew
		self.crew_max = crew_max

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
