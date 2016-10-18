from flask import *
import world_gen, math

app = Flask(__name__)

player_galaxy = world_gen.Galaxy()
player_galaxy.galaxy_generation()


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			# Execute the next turn.
			pass
	return render_template('template.html', player_galaxy=player_galaxy.dictionary_ify(), trim_blocks=True, lstrip_blocks=True)


@app.route('/trial')
def trial():
	return render_template('trial.html', player_galaxy=player_galaxy.dictionary_ify(), trim_blocks=True, lstrip_blocks=True)


@app.route('/next_turn', methods=['POST'])
def next_turn():
	jquery_data = request.get_json()

	player_galaxy.current_position = jquery_data['selected_position']
	current_chunk = [math.floor((player_galaxy.current_position[0] + 30) / 60), math.floor((player_galaxy.current_position[1] + 30) / 60)]
	if current_chunk != player_galaxy.current_chunk:
		player_galaxy.current_chunk = current_chunk
		player_galaxy.galaxy_segment_generation()

	return jsonify(refresh=True)

if __name__ == '__main__':
	app.run(debug=False)
