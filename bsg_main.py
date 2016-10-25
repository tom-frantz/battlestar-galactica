from flask import *
import galaxy_gen as galaxy
import navigation as nav
import math

# The Flask initialization.
app = Flask(__name__)

# Create the galaxy, need to assign to it to a world class eventually with other ai and shit.
player_galaxy = galaxy.Galaxy()
player_galaxy.initial_galaxy_generation()


# The code that happens for a page load for the base page
@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('template.html', player_galaxy=player_galaxy.dictionary_ify(), trim_blocks=True, lstrip_blocks=True)


# A dummy page for any element we're trialing.
@app.route('/trial')
def trial():
	return render_template('trial.html', player_galaxy=player_galaxy.dictionary_ify(), trim_blocks=True, lstrip_blocks=True)


# Code for a AJAX call for the next turn functions.
@app.route('/next_turn', methods=['POST'])
def next_turn():
	jquery_data = request.get_json()

	if jquery_data['next_turn_type'] == 'warp':
		player_galaxy.current_position = jquery_data['selected_position']
		current_chunk = [math.floor((player_galaxy.current_position[0] + 30) / 60), math.floor((player_galaxy.current_position[1] + 30) / 60)]
		if current_chunk != player_galaxy.current_chunk:
			player_galaxy.current_chunk = current_chunk
			player_galaxy.galaxy_chunk_generation()

	return jsonify(refresh=True)

if __name__ == '__main__':
	app.run(debug=True)
