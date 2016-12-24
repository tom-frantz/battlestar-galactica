# FOR NOTE: request.form[name] = value

from flask import *
import sqlite3
import json
import os
import pickle
from datetime import datetime, timedelta

import world
from modules import events, fleets
import modules.galaxy_gen as galaxy


def to_json(obj):
	return obj.__dict__


player_world = world.World(galaxy.Galaxy(), events.EventHandler(), fleets.FleetHandler(), datetime(1942, 7, 23, 8, 0, 0, 0))

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


# The code that happens for a page load for the base page. Contains the Main Menu HTML render as well as the core game.
@app.route('/', methods=['GET', 'POST'])
def index():
	if not player_world.world_initiated:
		if request.method == 'POST':
			seed = request.form.get('seed', None)
			if request.form.get('seed', None) == '':
				seed = False
			# POST's for new game
			if request.form.get('start_new_game', None) == 'default':
				player_world.initial_galaxy_generation(seed)
			elif request.form.get('start_new_game', None) == 'random':
				player_world.initial_galaxy_generation(seed, False)
		else:
			db = get_db()
			cur = db.execute('SELECT * FROM saves')
			saves = cur.fetchall()
			return render_template('index.html', saves=saves, trim_blocks=True, lstrip_blocks=True)

	db = get_db()
	cur = db.execute('SELECT * FROM saves')
	saves = cur.fetchall()

	if request.method == 'POST':
		pass
	return render_template('main.html', player_world=json.dumps(player_world, default=to_json), saves=saves,
						   trim_blocks=True, lstrip_blocks=True)


@app.route('/event_loop', methods=['GET'])
def events_fired():
	global player_world
	event_queue = request.get_json()

	player_world.event_loop(event_queue)
	return jsonify(player_world=player_world)


# To create a save game or modify it. Is executed in main.html
@app.route('/save_game', methods=['POST'])
def save_game():
	global player_world
	jquery_data = request.get_json()

	time = datetime.now()
	if time.minute < 10:
		time_minute = '0' + str(time.minute)
	else:
		time_minute = str(time.minute)
	time = str(time.day) + '/' + str(time.month) + '/' + str(time.year) + ' ' + str(time.hour) + ':' + time_minute

	db = get_db()
	cur = db.execute('SELECT save_name FROM saves')
	saves = cur.fetchall()

	for save in saves:
		if jquery_data['save_name'] == save['save_name']:
			db.execute('UPDATE saves SET pickle=?, modified_time=? WHERE save_name=?;',
					   (pickle.dumps(player_world), time, jquery_data['save_name']))
			db.commit()
			return jsonify(time=time)
	db.execute(
		'INSERT INTO saves (save_name, pickle, create_time, modified_time, save_settings) VALUES (?, ?, ?, ?, ?);',
		(jquery_data['save_name'], pickle.dumps(player_world), time, time, '{"seed": ' + str(player_world.seed) + '}'))
	db.commit()
	return jsonify(time=time)


# Code to check if a save is valid. Is executed in index.html
@app.route('/load_game', methods=['POST'])
def validate_save():
	global player_world
	jquery_data = request.get_json()

	db = get_db()
	cur = db.execute('SELECT pickle FROM saves WHERE save_name=?', [jquery_data['save_name']])
	player_save = cur.fetchone()

	if player_save:
		player_world = pickle.loads(player_save['pickle'])
		print(player_world.world_initiated)
		print('Save Valid')
		return jsonify(valid=True)
	print("Save Invalid")
	return jsonify(valid=False)


# Code for a AJAX call for the next turn functions.
@app.route('/next_turn', methods=['POST'])
def next_turn():
	jquery_data = request.get_json()

	player_world.next_turn(jquery_data)

	return jsonify(success=True)


@app.route('/trial')
def trial():
	return render_template("trial2.html")


if __name__ == '__main__':
	app.run()
