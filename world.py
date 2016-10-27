class World(object):
	def __init__(self, galaxy):
		self.galaxy = galaxy

	def world_serialize(self):
		world_dict = {
			'galaxy': self.galaxy.galaxy_serialize()
		}

		return world_dict
