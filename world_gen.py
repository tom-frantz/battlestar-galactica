import random

SYSTEM_NAMES = ('Abydos', 'Aegis', 'Aldebaran', 'Amel', 'Aurelia', 'Balaho', 'Ballybran', 'Belzagor', 'Chiron', 'Chthon', 'Corneria', 'Cyteen', 'Demeter', 'Deucalion', 'Dosadi', 'Eayn', 'Erna', 'Etheria', 'Fhloston', 'Finisterre', 'Furya', 'Gallifrey', 'Gor', "Gorta")
SYSTEM_NAMES_PREFIXES = ('Al', 'Omi', 'Bah')
SYSTEM_NAMES_SUFFIXES = ('Prime', 'Alpha', 'Beta', 'Delta', 'Gamma', 'Minor', '')


class SolarSystem(object):
	def __init__(self, position, name):
		self.global_position = position
		self.total_planets = random.randint(0, 8)
		self.planets = {}
		self.name = name

	def generate_planets(self):
		# Execute when system is jumped into.
		pass


class Galaxy(object):
	def __init__(self):
		self.planet_abundance = 'Placeholder'
		self.cylon_intensity = 'placeholder'
		self.system_list = {}
		self.current_position = (0, 0)

	def galaxy_generation(self):
		self.system_list['Helios Alpha'] = SolarSystem((0, 0), "Helios Alpha")
		for x in range(-30, 30):
			for y in range(-30, 30):
				system_chance = random.randint(1, 15)
				if system_chance == 1:
					system_too_close = False
					for system in self.system_list:
						if -1 <= x - self.system_list[system].global_position[0] <= 1 and -1 <= y - self.system_list[system].global_position[1] <= 1:
							system_too_close = True
					if not system_too_close:
						a = random.randint(1, 10)
						if a == 10:
							system_name = random.choice(SYSTEM_NAMES_PREFIXES) + ' ' + random.choice(SYSTEM_NAMES) + ' ' + random.choice(SYSTEM_NAMES_SUFFIXES)
						elif a == 9:
							system_name = random.choice(SYSTEM_NAMES_PREFIXES) + ' ' + random.choice(SYSTEM_NAMES)
						elif a == 8:
							system_name = random.choice(SYSTEM_NAMES) + ' ' + random.choice(SYSTEM_NAMES_SUFFIXES)
						else:
							system_name = random.choice(SYSTEM_NAMES)
						self.system_list[system_name] = SolarSystem((x, y), system_name)
						print(self.system_list[system_name].name, self.system_list[system_name].global_position)

	def galaxy_segment_generation(self):
		# execute this when there is no more galaxy, or closing in on no more galaxy left
		pass
