# Import all the events.
from static.events import the_fat_toaster_sings


events_list = [the_fat_toaster_sings]


class EventHandler(object):
	def __init__(self, world):
		self.world = world
		self.events = []
		for event_file in events_list:
			self.events.append(Event(event_file))


class Event(object):
	def __init__(self, event):
		self.id = event.event['id']
		self.title = event.event['title']
		self.dialogs = event.event['dialogs']
		self.outcomes = event.event['outcomes']
		self.function = event.function

	def effects(self):
		print(self.function('Test 1'))

	def event_html_serialize(self):
		event_dict = {
			'title': self.title,
			'dialogs': self.dialogs,
			'outcomes': self.outcomes,
			'id': self.id
		}
		return event_dict

event_handler = EventHandler('world_obj')
print(event_handler.events[0].effects())
