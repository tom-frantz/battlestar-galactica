from flask import *
import random

# Papa Phillipo is a real dank meme
app = Flask(__name__)


class Galaxy(object):
	def __init__(self):
		self.galaxy_x_axis = [-100, 100]
		self.galaxy_y_axis = [-100, 100]
		self.planet_abundance = 'Placeholder'
		self.cylon_intensity = 'placeholder'
		self.system_list = {0: (-2, -2)}

	def galaxy_generation(self):
		system_generated = 1
		for x in range(-100, 100):
			for y in range(-100, 100):
				z = random.randint(1, 15)
				if z == 5:
					planet_too_close = False
					for planet in self.system_list:
						if -1 <= x - self.system_list[planet][0] <= 1:
							if -1 <= y - self.system_list[planet][1] <= 1:
								planet_too_close = True
					if planet_too_close:
						pass
						# print("planet not generated at: (" + str(x) + "," , str(y) )
					else:
						self.system_list[system_generated] = [x, y]
						# print(self.system_list[system_generated])
						system_generated += 1

	def galaxy_segment_generation(self):
		# execute this when there is no more galaxy, or closing in on no more galaxy left
		pass

player_galaxy = Galaxy()
player_galaxy.galaxy_generation()


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		if request.form['submit'] == 'next_turn':
			pass
	return render_template('index.html', player_galaxy=player_galaxy)


@app.route('/map', methods=['GET', 'POST'])
def map():
	if request.method == 'POST':
		pass
	return render_template('map.html', player_galaxy=player_galaxy)


@app.route('/canvas', methods=['GET', 'POST'])
def canvas():
	if request.method == 'POST':
		pass
	return render_template('canvas.html', player_galaxy=player_galaxy)


if __name__ == '__main__':
	app.run(debug=True)
