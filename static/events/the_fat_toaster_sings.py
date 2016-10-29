event = {
	'id': '0',
	'title': 'The Fat Toaster Sings',
	'dialogs': {
		'0': {  # It will always load dialog 0 initially.
			'text': 'Flavour text for the anomaly on initial load', # flavour text.
			'options': [{
				# option 1 for first dialog
				'type': 'dialogs',  # Either dialog (Another option box) or outcome, which pops a final box and ends the event chain.
				'path': '1',  # What dialog or outcome it pops
				'text': 'Flavour text for a dialog (1)'  # Flavour text
			}, {
				# option 2 first dialog
				'type': 'dialogs',
				'path': '1',
				'text': 'Flavour text for another dialog (2)'
			}]
		},
		'1': {
			'text': "Flavour text for option 1",
			'options': [{
				# option 1 for dialog 1
				'type': 'outcomes',
				'path': '0',
				'text': 'Flavour text for an outcome (0)'
			}]
		},
	},
	'outcomes': {
		'0': {
			'text': 'Flavour text for outcome 0',
			'outcome': [
				['Negative effect', 'text-danger'],  # Flavour text, the text class.
				['Positive effect', 'text-success']
			]  # integration with main for when effects come into play.
		}
	}
}


def function(string):
	return string
