# Import all the events.
from static.events import the_fat_toaster_sings
from static.events.anomalies import escape_pod


EVENTS_LIST = [the_fat_toaster_sings]


class EventHandler(object):
	def __init__(self):
		self.events = []
		for event_file in EVENTS_LIST:
			self.events.append(StoryEvent(event_file))


class StoryEvent(object):
	def __init__(self, event):
		self.ID = event.event['ID']
		self.title = event.event['title']
		self.nodes = event.event['nodes']
		self.outcomes = event.event['outcomes']
		self.function = event.function

	def effects(self, world):
		self.function(world)
