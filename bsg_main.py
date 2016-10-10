from flask import *
import world_gen

app = Flask(__name__)

player_galaxy = world_gen.Galaxy()


def next_turn():
	pass


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			pass
	return render_template('index.html')


@app.route('/map', methods=['GET', 'POST'])
def star_map():
	player_galaxy.galaxy_generation()
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			pass
	system_list = {}
	for system in player_galaxy.system_list:
		if player_galaxy.current_position[0] - 30 <= player_galaxy.system_list[system].global_position[0] <= player_galaxy.current_position[0] + 30 \
		and player_galaxy.current_position[1] - 30 <= player_galaxy.system_list[system].global_position[1] <= player_galaxy.current_position[0] + 30:
			system_list[system] = player_galaxy.system_list[system]
	return render_template('map_clone.html', system_list=system_list, current_position=player_galaxy.current_position, trim_blocks=True, lstrip_blocks=True)

if __name__ == '__main__':
	app.run(debug=True)
