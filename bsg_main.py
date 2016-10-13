from flask import *
import world_gen, json

app = Flask(__name__)

player_galaxy = world_gen.Galaxy()
player_galaxy.galaxy_generation()


def next_turn():
	player_galaxy.galaxy_segment_generation()


def galaxy_to_dict(Galaxy):
	galaxy_dict = {}
	return galaxy_dict


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			# Execute the next turn.
			pass
	system_list = {}
	# for system in player_galaxy.system_list:
	# 	if player_galaxy.current_position[0] - 30 <= player_galaxy.system_list[system].global_position[0] <= player_galaxy.current_position[0] + 30 \
	# 	and player_galaxy.current_position[1] - 30 <= player_galaxy.system_list[system].global_position[1] <= player_galaxy.current_position[0] + 30:
	# 		system_list[system] = player_galaxy.system_list[system]

	dict_player_galaxy = player_galaxy.dictionary_ify()
	return render_template('template.html', system_list=system_list, player_galaxy=dict_player_galaxy, trim_blocks=True, lstrip_blocks=True)


@app.route('/map', methods=['GET', 'POST'])
def star_map():
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			# Execute next turn
			pass
	system_list = {}
	for system in player_galaxy.system_list:
		if player_galaxy.current_position[0] - 30 <= player_galaxy.system_list[system].global_position[0] <= player_galaxy.current_position[0] + 30 \
		and player_galaxy.current_position[1] - 30 <= player_galaxy.system_list[system].global_position[1] <= player_galaxy.current_position[0] + 30:
			system_list[system] = player_galaxy.system_list[system]
	return render_template('map_clone.html', system_list=system_list, current_position=player_galaxy.current_position, trim_blocks=True, lstrip_blocks=True)

if __name__ == '__main__':
	app.run(debug=False)
