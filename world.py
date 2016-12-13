import math
import random


class World(object):
	def __init__(self, galaxy, event_handler, fleet_handler):
		self.galaxy = galaxy
		self.event_handler = event_handler
		self.fleet_handler = fleet_handler

		self.world_initiated = False
		self.seed = random.seed(random.randint(-4294967295, 4294967295))
		self.next_turn_actions = {
			'warp': self.warp
		}

	def initial_galaxy_generation(self, seed, galaxy_gen_default=True):
		self.galaxy.initial_galaxy_generation(galaxy_gen_default)
		self.fleet_handler.generate_battlestar(local_location='Caprica')
		if seed or seed == 0:
			self.seed = seed
		self.world_initiated = True

	def next_turn(self, json_data):
		for action in json_data['actions']:
			action_function = json_data['actions'][action]
			try:
				getattr(self, action_function[0])(action_function[1])
			except KeyError as error:
				print('Key not recognised in "self.next_turn_actions": ' + str(error))

	def warp(self, parameters):
		a = parameters['selected_position'][0] - self.galaxy.current_position[0]
		b = parameters['selected_position'][1] - self.galaxy.current_position[1]

		warp_range = math.sqrt((a ** 2) + (b ** 2))
		warp_success_threshold = random.randint(20, 40)

		if warp_range <= warp_success_threshold:
			self.__warp_success(parameters)
		elif warp_range - warp_success_threshold < 4:
			# Add in stuff for undesired orbit, near other body
			self.__warp_success(parameters)
		elif warp_range - warp_success_threshold < 10:
			# Add stuff for unstable orbit, headed to/from body
			self.__warp_success(parameters)
		elif warp_range - warp_success_threshold < 20:
			# Add stuff for fleet being spread out.
			self.__warp_success(parameters)
		else:
			# Fleet Dies, warp into planet/sun
			warp_success = False

	def __warp_success(self, parameters):
		if parameters['fleet']['primary_fleet']:
			self.galaxy.current_position = parameters['selected_position']
			current_chunk = [math.floor((self.galaxy.current_position[0] + 30) / 60), math.floor((self.galaxy.current_position[1] + 30) / 60)]
			if current_chunk != self.galaxy.current_chunk:
				self.galaxy.current_chunk = current_chunk
				self.galaxy.galaxy_chunk_generation()
