# FOR NOTE: request.form[name] = value

from flask import *
import world
import modules.galaxy_gen as galaxy
from modules import events, fleets

# The Flask initialization.
app = Flask(__name__)
player_world = world.World(galaxy.Galaxy(), events.EventHandler(), fleets.FleetHandler())


@app.route('/menu', methods=['GET', 'POST'])
def menu():
	if request.method == 'POST':
		if request.form.get('start_game', None) == 'default':
			player_world.initial_galaxy_generation()
		elif request.form.get('start_game', None) == 'random':
			player_world.initial_galaxy_generation(False)
		return redirect('/')
	return render_template('index.html', trim_blocks=True, lstrip_blocks=True)


# The code that happens for a page load for the base page
@app.route('/', methods=['GET', 'POST'])
def index():
	if not player_world.galaxy.initiated:
		return redirect('/menu')
	return render_template('template.html', player_world=player_world.world_serialize(), trim_blocks=True, lstrip_blocks=True)


# A dummy page for any element we're trialing.
@app.route('/trial')
def trial():
	return render_template('trial.html', player_world=player_world.world_serialize(), event=player_world.event_handler.events[0].event_html_serialize(), trim_blocks=True, lstrip_blocks=True)


# Code for a AJAX call for the next turn functions.
@app.route('/next_turn', methods=['POST'])
def next_turn():
	jquery_data = request.get_json()

	player_world.next_turn(jquery_data)

	return jsonify(success=True)


# Code for an AJAX call for the end of an event.
@app.route('/event_finished', methods=['POST'])
def event_finished():
	jquery_data = request.get_json()

	print(jquery_data['event_history'])
	# Do the event id fire thing.

	return jsonify(success=True)


if __name__ == '__main__':
	app.run(debug=True)
