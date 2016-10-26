import random
import math
import roman


# STATIC VARS.
SYSTEM_NAMES = ('Abydos', 'Aegis', 'Aldebaran', 'Amel', 'Aurelia', 'Balaho', 'Ballybran', 'Belzagor', 'Chiron', 'Chthon', 'Corneria', 'Cyteen', 'Demeter', 'Deucalion', 'Dosadi', 'Eayn', 'Erna', 'Etheria', 'Fhloston', 'Finisterre', 'Furya', 'Gallifrey', 'Gor', "Gorta")
SYSTEM_NAMES_PREFIXES = ('Al', 'Omi', 'Bah')
SYSTEM_NAMES_SUFFIXES = ('Prime', 'Alpha', 'Beta', 'Delta', 'Gamma', 'Minor')

# There needs to be at least two entries per var to make sure the random.choice works properly
STARS = (
	['Blue Dwarf', ['/static/images/stars/B_D_1.png']],
	['Blue Giant', ['/static/images/stars/B_G_1.png']],
	['Blue Main', ['/static/images/stars/B_M_1.png']],
	['Red Dwarf', ['/static/images/stars/R_D_1.png']],
	['Red Giant', ['/static/images/stars/R_G_1.png']],
	['Red Main', ['/static/images/stars/R_M_1.png']],
	['Red Super Giant', ['/static/images/stars/R_SG_1.png']],
	['Yellow Main', ['/static/images/stars/Y_M_1.png']]
)

PLANETS = (
	['Barren', ['/static/images/planets/BAR_1.png']],
	['Barren', ['/static/images/planets/BAR_1.png']]
)

MOONS = (
	['Rocky', ['/static/images/moons/ROC_1.png']],
	['Rocky', ['/static/images/moons/ROC_1.png']]
)

ASTEROIDS = (
	['Small Belt', ['/static/images/asteroids/SMA_1.png']],
	['Small Belt', ['/static/images/asteroids/SMA_1.png']]
)

COMETS = (
	['Ice', ['/static/images/comets/ICE.png']],
	['Ice', ['/static/images/comets/ICE.png']]
)


class Galaxy(object):
	def __init__(self):
		self.chunks_loaded = [[-1, 1], [-1, 0], [-1, 1], [0, -1], [0, 0], [0, 1], [1, -1], [1, 0], [1, 1]]
		# Change this to a list for ease of access. Solar systems have name/global coords for information lost.
		self.system_list = []
		self.current_position = [0, 0]
		self.current_chunk = [0, 0]

	def initial_galaxy_generation(self):
		# Generate the initial 3x3 chunk
		self.system_list = []
		self.system_list.append(SolarSystem((0, 0), "Helios Alpha", total_planets=4))
		self.system_list[0].generate_bodies()
		self.__create_solar_systems([-90, 90], [-90, 90])

	def galaxy_chunk_generation(self):
		gen_list = []
		# -1 and +2 are to ensure that the range works properly from the current chunk and does not cut out the border chunks.
		for x in range(self.current_chunk[0] - 1, self.current_chunk[0] + 2):
			for y in range(self.current_chunk[1] - 1, self.current_chunk[1] + 2):
				gen_list.append([x, y])

		for chunk in gen_list:
			if chunk not in self.chunks_loaded:
				self.__create_solar_systems([chunk[0] * 60 - 30, chunk[0] * 60 + 30], [chunk[1] * 60 - 30, chunk[1] * 60 + 30])
				self.chunks_loaded.append(chunk)

	def __create_solar_systems(self, x_bounds, y_bounds, chance=20):
		total_count = 0
		# +1 is to ensure that the range works properly and does not cut out the extra border.
		for x in range(x_bounds[0], x_bounds[1] + 1):
			for y in range(y_bounds[0], y_bounds[1] + 1):
				system_chance = random.randint(0, chance)
				if system_chance == 0:

					# Check if the generated system is too close to any other created systems.
					system_too_close = False
					for system in self.system_list:
						if -1 <= x - system.global_position[0] <= 1 and -1 <= y - system.global_position[1] <= 1:
							system_too_close = True

					# Name and create the system
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
						solar_system = SolarSystem((x, y), system_name)
						self.system_list.append(solar_system)
						print(self.system_list[self.system_list.index(solar_system)].name, self.system_list[self.system_list.index(solar_system)].global_position)
						total_count += 1

		print('Total Count:', total_count)

	def dictionary_ify(self):
		# OUT OF DATE!
		galaxy_dict = {
			'chunks_loaded': self.chunks_loaded,
			'current_position': self.current_position,
			'system_list': {},
			'current_chunk': self.current_chunk
		}
		for sys in self.system_list:
			galaxy_dict['system_list'][sys.global_position] = {
				'name': self.system_list[sys].name,
				'global_position': self.system_list[sys].global_position,
				'total_planets': self.system_list[sys].total_planets,
				'star_type': self.system_list[sys].star_type,
				'star_file': self.system_list[sys].star_file,
				'planets': self.system_list[sys].planets,
				'visited': self.system_list[sys].visited
			}
		return galaxy_dict


class SolarSystem(object):
	def __init__(self, position, name, **kwargs):
		# Generating key information
		self.global_position = [position[0], position[1]]
		self.total_planets = random.randint(0, 8)
		self.bodies = []
		self.name = name

		# Choosing a star and assigning it.
		star = random.choice(STARS)
		self.type = star[0]
		self.file = star[1]

		# History of the star.
		self.visited = 'never'

		# Updating any specific args.
		self.__dict__.update(kwargs)

	def generate_bodies(self, asteroid_chance=10):
		# Generate planets and asteroids for a solar system. Call when necessary, not on generation of the system.
		for orbit_index in range(0, self.total_planets):
			body_name = self.name + " " + roman.toRoman(orbit_index + 1)
			if random.randint(1, asteroid_chance) == 1:
				# Generate asteroids
				self.bodies.append(CelestialBody(body_name, ASTEROIDS, orbit_index))
			else:
				# generate planet
				self.bodies.append(Planet(body_name, PLANETS, orbit_index))
			print(self.bodies[orbit_index].name)


# Basis for Comets, Asteroids, Planets, Moons or any other object located within a system.
# Instantiate this for asteroid belts and for comets.
class CelestialBody(object):
	def __init__(self, name, BODY, orbit, **kwargs):
		self.name = name

		# for resources, [Abundance, Amount available]. Can increase amount available from planets and moons.
		self.resources = {
			'water': [random.randint(0, 1), 100],
			'food': [random.randint(0, 1), 100],
			'tylium_ore': [random.randint(0, 1), 100],
			'aluminium': [random.randint(0, 1), 100],
			'copper': [random.randint(0, 1), 100],
			'iron': [random.randint(0, 1), 100],
			'uranium': [random.randint(0, 1), 100],
			'carbon': [random.randint(0, 1), 100],
			'oils': [random.randint(0, 1), 100],
			'isotopic_minerals': [random.randint(0, 1), 100]
		}

		# Assigning what body it will be. (Aster, Comet, Planet, Moon)
		body = random.choice(BODY)
		self.type = body[0]
		self.file = random.choice(body[1])

		# 0 to n for objects that orbit sun (Planets and asteroid belts), and -1 for comets. Moons have 0 to n for their orbits around parent planet.
		self.parent_body = 'Star'
		self.orbit = orbit
		self.__dict__.update(kwargs)


# Basis for Planets and Moons
# Instantiate this for moons
class TerrestrialBody(CelestialBody):
	def __init__(self, name, BODY, orbit, anomaly_chance=10, **kwargs):
		super().__init__(name, BODY, orbit)
		self.visited = 'never'

		# code for anomaly. Generate inside __init__ function
		# base one in ten chance of creating anomaly.
		if random.randint(1, anomaly_chance) == 1:
			pass

		self.__dict__.update(kwargs)


class Planet(TerrestrialBody):
	def __init__(self, name, BODY, orbit, **kwargs):
		super().__init__(name, BODY, orbit)

		# Moon Generation
		self.moons = []
		for orbit_index in range(0, random.randint(0, 4)):
			# Need to fix moon naming.
			name = self.name + " MOON " + str(orbit_index)
			self.moons.append(TerrestrialBody(name, MOONS, orbit_index))

		self.__dict__.update(kwargs)
