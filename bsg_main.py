# FOR NOTE: request.form[name] = value

from flask import *
import sqlite3
import random, json, os

import world
from modules import events, fleets
import modules.galaxy_gen as galaxy


def to_json(obj):
	return obj.__dict__

# The Flask initialization.
app = Flask(__name__)
app.config.from_object('flask_config')

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'player_database.db')
))


def connect_db():
	# Connects to the specific database.
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()


@app.cli.command('initdb')
def initdb_command():
	# Initializes the DB
	init_db()
	print('Initialized the database.')


def get_db():
	# Opens a new database connection if there is none for the current app context.
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


player_world = world.World(galaxy.Galaxy(), events.EventHandler(), fleets.FleetHandler())


# The code that happens for a page load for the base page. Contains the Main Menu HTML render as well as the core game.
@app.route('/', methods=['GET', 'POST'])
def index():
	if not player_world.initiated:
		if request.method == 'POST':
			seed = request.form.get('seed', None)
			if request.form.get('seed', None) == '':
				seed = False

			if request.form.get('start_game', None) == 'default':
				player_world.initial_galaxy_generation(seed)
			elif request.form.get('start_game', None) == 'random':
				player_world.initial_galaxy_generation(seed, False)

		else:
			return render_template('index.html', trim_blocks=True, lstrip_blocks=True)

	if request.method == 'POST':
		pass
	return render_template('main.html', player_world=json.dumps(player_world, default=to_json), trim_blocks=True, lstrip_blocks=True)


# A dummy page for any element we're trialing.
@app.route('/trial')
def trial():
	return render_template('trial.html', player_world=json.dumps(player_world, default=to_json), trim_blocks=True, lstrip_blocks=True)


@app.route('/database_trial')
def database_trial():
	db = get_db()
	db.execute('INSERT INTO players (title, text) VALUES (?, ?)', ['Walshy is', 'A MemeSlut(TM)'])
	db.commit()
	return ""


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
	app.run()
