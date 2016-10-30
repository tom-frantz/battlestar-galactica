event = {
	'ID': '0',
	'title': 'The Fat Toaster Sings',
	'nodes': {
		'0': {  # It will always load dialog 0 initially.
			'body_text': 'Flavour text for the event on initial load', # flavour text.
			'paths': [{
				# option 1 for first dialog
				'button_text': 'Flavour text for a dialog (1)',  # Flavour text
				'path': ['nodes', '1']  # What dialog or outcome it pops
			}, {
				# option 2 first dialog
				'button_text': 'Flavour text for another dialog (2)',
				'path': ['nodes', '2']
			}]
		},

		'1': {
			'body_text': "Flavour text for option 1",
			'paths': [{
				# option 1 for dialog 1
				'button_text': 'Flavour text for an outcome (0)',
				'path': ['outcomes', '0']
			}]
		},

		'2': {
			'body_text': 'Flavour text for option 2',
			'paths': [{
				'button_text': 'Flavour Text for an outcome (0)',
				'path': ['outcomes', '0']
			}]
		}
	},
	'outcomes': {
		'0': {
			'body_text': 'Flavour text for outcome 0',
			'effects': [
				['Negative effect', 'text-danger'],  # Flavour text, the text class.
				['Positive effect', 'text-success']
			]  # integration with main for when effects come into play.
		}
	}
}


def function(world, event_chain, outcome):
	pass
