import sqlite3
import click
from flask import current_app, g

def get_db():
	'''
    Retrieve the SQLite DB connection stored in Flask's `g` 
    context variable. If no connection exists, open one and store it.
    '''
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row
	return g.db


def close_db(e=None):
	'''
	Close the DB connection at the end of the request, if it exists.
	'''
	db = g.pop('db', None)
	if db is not None:
		db.close()


def init_db():
	'''
    Initialize the DB using schema.sql.
    This drops and recreates tables as defined in the SQL script.
    '''
	db = get_db()
	with current_app.open_resource("schema.sql") as f:
		db.executescript(f.read().decode("utf-8"))


@click.command("init-db")
def init_db_command():
	'''
    Flask CLI command to initialize the DB by running schema.sql.
    Run `flask --app llm_app init-db` the first time you use the app.
    '''
	init_db()
	click.echo("Initialized the database")


def init_app(app):
	'''
    Register DB-related functions with the app:
    	- Ensure the DB connection is closed after each request.
    	- Add CLI command for DB initialization.
    '''
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
