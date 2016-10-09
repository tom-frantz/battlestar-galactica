from flask import *
import world_gen

app = Flask(__name__)

player_galaxy = world_gen.Galaxy()
player_galaxy.galaxy_generation()


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			pass
	return render_template('index.html')


@app.route('/map', methods=['GET', 'POST'])
def star_map():
	# Need algorithm for making global to local. Return values from 0 to 60
	player_galaxy.galaxy_generation()
	if request.method == 'POST':
		pass
	return render_template('map_clone.html', player_galaxy=player_galaxy, trim_blocks=True, lstrip_blocks=True)

if __name__ == '__main__':
	app.run(debug=True)
