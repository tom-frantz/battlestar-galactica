anomaly = {
	'title': 'The Fat Toaster Sings',
	'dialogs': {
		0: {  # It will always load dialog 0 initially.
			'text': 'Flavour text for the anomaly on initial load', # flavour text.
			'options': [{
				# option 1 for first dialog
				'type': 'dialogs',  # Either dialog (Another option box) or outcome, which pops a final box and ends the event chain.
				'path': 1,  # What dialog or outcome it pops
				'text': 'Flavour text for an dialog (1)'  # Flavour text
			}, {
				# option 2 first dialog
				'type': 'dialogs',
				'path': 1,
				'text': 'Flavour text for another dialog (2)'
			}]
		},
		1: {
			'text': "Flavour text for option 1",
			'options': [{
				# option 1 for dialog 1
				'type': 'outcomes',
				'path': 0,
				'text': 'Flavour text for '
			}]
		},
	},
	'outcomes': {
		0: {
			'text': 'Flavour text for outcome',
			'outcome': ''  # integration with main for when effects come into play.
		}
	}
}


# Standard anomaly run:
def run_event(event):
	end_of_event = False
	while not end_of_event:
		pass
