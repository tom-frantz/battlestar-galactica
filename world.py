class World(object):
	def __init__(self, galaxy, event_handler):
		self.galaxy = galaxy
		self.event_handler = event_handler

	def world_serialize(self):
		world_dict = {
			'galaxy': self.galaxy.galaxy_serialize()
		}

		return world_dict
