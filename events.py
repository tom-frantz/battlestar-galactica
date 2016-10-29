# Import all the events.
from static.events import the_fat_toaster_sings
from static.events.anomalies import escape_pod


EVENTS_LIST = [the_fat_toaster_sings]


class EventHandler(object):
	def __init__(self):
		self.events = []
		for event_file in EVENTS_LIST:
			self.events.append(Event(event_file))


class Event(object):
	def __init__(self, event):
		self.ID = event.event['ID']
		self.title = event.event['title']
		self.nodes = event.event['nodes']
		self.outcomes = event.event['outcomes']
		self.function = event.function

	def effects(self, world):
		self.function(world)

	def event_html_serialize(self):
		event_dict = {
			'title': self.title,
			'nodes': self.nodes,
			'outcomes': self.outcomes,
			'ID': self.ID
		}
		return event_dict
