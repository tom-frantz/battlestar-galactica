from flask import *
import random

# Papa Phillipo is a real dank meme
app = Flask(__name__)


class Galaxy(object):
	def __init__(self, galaxy_size):
		self.galaxy_size = galaxy_size
		self.planet_abundance = 'Placeholder'
		self.cylon_intensity = 'placeholder'
		self.system_list = {0: (-2, -2)}

	def galaxy_generation(self):
		system_generated = 1

		for x in range(self.galaxy_size):
			for y in range(self.galaxy_size):
				z = random.randint(1,15)
				if z == 5:
					planet_too_close = False
					for planet in self.system_list:
						if -1 <= x - self.system_list[planet][0] <= 1:
							if -1 <= y - self.system_list[planet][1] <= 1:
								planet_too_close = True
					if planet_too_close:
						print("planet not generated at: (" + str(x) + "," , str(y) )
					else:
						self.system_list[system_generated] = (x, y)
						print(self.system_list[system_generated])
						system_generated += 1

player_galaxy = Galaxy(20)


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
