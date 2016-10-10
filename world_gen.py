import random
import math

SYSTEM_NAMES = ('Abydos', 'Aegis', 'Aldebaran', 'Amel', 'Aurelia', 'Balaho', 'Ballybran', 'Belzagor', 'Chiron', 'Chthon', 'Corneria', 'Cyteen', 'Demeter', 'Deucalion', 'Dosadi', 'Eayn', 'Erna', 'Etheria', 'Fhloston', 'Finisterre', 'Furya', 'Gallifrey', 'Gor', "Gorta")
SYSTEM_NAMES_PREFIXES = ('Al', 'Omi', 'Bah')
SYSTEM_NAMES_SUFFIXES = ('Prime', 'Alpha', 'Beta', 'Delta', 'Gamma', 'Minor', '')


class SolarSystem(object):
	def __init__(self, position, name, total_planets=False):
		self.global_position = position
		if not total_planets and total_planets != 0:
			self.total_planets = random.randint(0, 8)
		else:
			self.total_planets = total_planets
		self.planets = {}
		self.name = name

	def generate_planets(self):
		# Execute when system is jumped into.
		pass


class Galaxy(object):
	def __init__(self):
		self.chunks_loaded = [[-1, 1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
		self.planet_abundance = 'Placeholder'
		self.cylon_intensity = 'placeholder'
		self.system_list = {}
		self.current_position = [0, 0]

	def galaxy_generation(self):
		self.system_list = {}
		self.system_list['Helios Alpha'] = SolarSystem((0, 0), "Helios Alpha", 4)
		self.create_solar_systems([-90, 90], [-90, 90])

	def galaxy_segment_generation(self):
		current_chunk = [math.floor(self.current_position[0]/30), math.floor(self.current_position[1]/30)]
		gen_list = []
		for x in range(current_chunk[0] - 1, current_chunk[0] + 2):
			for y in range(current_chunk[1] - 1, current_chunk[1] + 2):
				gen_list.append([x, y])
		for chunk in gen_list:
			if chunk not in self.chunks_loaded:
				self.create_solar_systems([chunk[0] * 60 - 30, chunk[0] * 60 + 30], [chunk[1] * 60 - 30, chunk[1] * 60 + 30])
				self.chunks_loaded.append(chunk)

	def create_solar_systems(self, x_bounds, y_bounds, chance=10):
		total_count = 0
		for x in range(x_bounds[0], x_bounds[1]):
			for y in range(y_bounds[0], y_bounds[1]):
				system_chance = random.randint(1, chance)
				if system_chance == 1:
					system_too_close = False
					for system in self.system_list:
						if -1 <= x - self.system_list[system].global_position[0] <= 1 and -1 <= y - self.system_list[system].global_position[1] <= 1:
							system_too_close = True
					if not system_too_close:
						name_chance = random.randint(1, 20)
						if name_chance == 10:
							system_name = random.choice(SYSTEM_NAMES_PREFIXES) + ' ' + random.choice(SYSTEM_NAMES) + ' ' + random.choice(SYSTEM_NAMES_SUFFIXES)
						elif name_chance == 9:
							system_name = random.choice(SYSTEM_NAMES_PREFIXES) + ' ' + random.choice(SYSTEM_NAMES)
						elif name_chance == 8:
							system_name = random.choice(SYSTEM_NAMES) + ' ' + random.choice(SYSTEM_NAMES_SUFFIXES)
						else:
							system_name = random.choice(SYSTEM_NAMES)
						self.system_list[system_name] = SolarSystem((x, y), system_name)
						print(self.system_list[system_name].name, self.system_list[system_name].global_position)
						total_count += 1
		print('Total Count:', total_count)
