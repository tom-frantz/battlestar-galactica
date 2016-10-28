from static.events import the_fat_toaster_sings


class Event(object):
	def __init__(self, event):
		self.title = event['title']
		self.dialogs = event['dialogs']
		self.outcomes = event['outcomes']

	def run_event(self):
		pass

	def event_serialize(self):
		event_dict = {
			'title': self.title,
			'dialogs': self.dialogs,
			'outcomes': self.outcomes
		}

		return event_dict

fat_event = Event(the_fat_toaster_sings.anomaly)
