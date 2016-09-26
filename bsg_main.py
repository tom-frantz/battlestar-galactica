from flask import *
import random

# Papa Phillipo is a real dank meme
app = Flask(__name__)


class Galaxy(object):
	def __init__(self, galaxy_size):
		self.galaxy_size = galaxy_size
		self.planet_abundance = 'Placeholder'
		self.cylon_intensity = 'placeholder'
		self.system_list = {}

	def galaxy_generation(self):
		system_generated = 1

		for x in range(self.galaxy_size):
			for y in range(self.galaxy_size):
				z = random.randint(1,20)
				if z == 5:
					self.system_list[system_generated] = (x, y)
					print(self.system_list[system_generated])
					system_generated += 1

player_galaxy = Galaxy(10)


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			pass
	return render_template('index.html')


@app.route('/map', methods=['GET', 'POST'])
def map():
	if request.method == 'POST':
		pass
	player_galaxy.galaxy_generation()
	return render_template('map.html', player_galaxy=player_galaxy)


if __name__ == '__main__':
	app.run(debug=True)
