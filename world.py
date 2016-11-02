import math


class World(object):
	def __init__(self, galaxy, event_handler, fleet_handler):
		self.galaxy = galaxy
		self.event_handler = event_handler
		self.fleet_handler = fleet_handler

	def next_turn(self, user_data):
		# user_data = {'selected_position': galaxy.system_list[system].global_coordinates}

		# Figure out how warp went
		self.galaxy.current_position = user_data['selected_position']

		# If warp moved fleet outside of the system, do this code to generate new part of galaxy
		current_chunk = [math.floor((self.galaxy.current_position[0] + 30) / 60), math.floor((self.galaxy.current_position[1] + 30) / 60)]
		if current_chunk != self.galaxy.current_chunk:
			self.galaxy.current_chunk = current_chunk
			self.galaxy.galaxy_chunk_generation()

	def world_serialize(self):
		world_dict = {
			'galaxy': self.galaxy.galaxy_serialize()
		}

		return world_dict

	def initial_galaxy_generation(self, galaxy_gen_default=True):
		self.galaxy.initial_galaxy_generation(galaxy_gen_default)
		self.fleet_handler.generate_colonial_fleet(galaxy_gen_default)
