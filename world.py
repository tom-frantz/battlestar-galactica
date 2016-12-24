import math
import random
from datetime import datetime, timedelta


class Event(object):
	def __init__(self, event_id, ticks, tick_measure, params):
		self.ticks_until_completion =  ticks
		self.event_id = event_id # The name of the method it will fire
		self.tick_measure = tick_measure # 'monthly', 'daily', 'hourly' ...
		self.event_params = params

class World(object):
	def __init__(self, galaxy, event_handler, fleet_handler, tick):
		self.galaxy = galaxy
		self.event_handler = event_handler
		self.fleet_handler = fleet_handler

		self.world_initiated = False
		self.seed = random.seed(random.randint(-4294967295, 4294967295))

		self.tick = tick
		self.event_queue = []

		self.clientside_events = {
			'warp': self.warp
		}

	def initial_galaxy_generation(self, seed, galaxy_gen_default=True):
		# TODO This functionality needs to be merged within the __init methods.
		self.galaxy.initial_galaxy_generation(galaxy_gen_default)
		self.fleet_handler.generate_battlestar(local_location='Caprica')
		if seed or seed == 0:
			self.seed = seed
		self.world_initiated = True

	def __tick_event(self, event):
		event.ticks_until_completion -= 1
		if event.ticks_until_completion == 0:
			getattr(self.clientside_events, event['event_id'])(event['event_params'])
			self.event_queue.remove(event)

	def event_loop(self, clientside_events):
		# DONE Event management from ajax call
		for event in clientside_events:
			cur_event = clientside_events[event]
			self.event_queue.append(Event(cur_event['event_id'], cur_event['ticks_until_completion'], cur_event['tick_measure'], cur_event['event_params']))

		tick_old_day = self.tick.days
		tick_old_month = self.tick.month
		self.tick = self.tick + timedelta(hours=1)
		if self.tick.month != tick_old_month:
			for event in self.event_queue:
				self.__tick_event(event)
		elif self.tick.days != tick_old_day:
			for event in self.event_queue:
				if event.tick_measure != 'monthly':
					self.__tick_event(event)
		else:
			for event in self.event_queue:
				if event.tick_measure == 'hourly':
					self.__tick_event(event)

		# TODO The maintenance costs, etc for every hour/day/month.

	def warp(self, params):
		# Params given: 'target_fleet_id', 'target_location', 'current_location'
		for fleet in self.fleet_handler['fleets']:
			if fleet.fleet_id == params['target_fleet_id']:
				target_fleet = fleet
				break
		target_location = params['target_location']
		current_location = params['current_location']
		# TODO Everything to do with warp.

		self.clientside_updates_list['Refresh'] = True

	def __warp_success(self, parameters):
		# TODO Complete this shit.
		if parameters['fleet']['primary_fleet']:
			self.galaxy.current_position = parameters['selected_position']
			current_chunk = [math.floor((self.galaxy.current_position[0] + 30) / 60), math.floor((self.galaxy.current_position[1] + 30) / 60)]
			if current_chunk != self.galaxy.current_chunk:
				self.galaxy.current_chunk = current_chunk
				self.galaxy.galaxy_chunk_generation()
