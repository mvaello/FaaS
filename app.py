#!flask/bin/python
# -*- coding: utf-8 -*-
"""
    Fortunes as a Service (faas)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A simple but useful REST service. Just for fun.
    
"""

import os
from flask import Flask, jsonify, g
import json
import sqlite3 as q
import random

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE = os.path.join(app.root_path,'fortunes.db'),
    DEBUG = True
))
app.config.from_envvar('FAAS_SETTINGS', silent = True)

def connect_db():
    """Connects to the databse"""
    con = q.connect(app.config['DATABASE'])
    con.row_factory = q.Row
    return con

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# Retive all fortunes stored in the DDBB
@app.route('/fortunes/api/v1.0/all', methods = ['GET'])
def get_all():
    db = get_db()
    cur = db.execute('select * from fortunes order by id asc')
    recs = cur.fetchall()
    rows = [ dict(rec) for rec in recs] 
    rows_json = json.dumps(rows, sort_keys=True, indent=4, separators=(',',': '))
    #print rows_json
    return rows_json

# Just retive a fortune
@app.route('/fortunes/api/v1.0/<int:fortune_id>', methods = ['GET'])
def get_by_id(fortune_id):
    # respone = filter(lambda t: t['id'] == fortune_id, fortunes)
    db = get_db()
    cur = db.execute("select * from fortunes where id = '%i'" % fortune_id)
    res = cur.fetchall()
    return jsonify({'fortunes': res})

@app.route('/fortunes/api/v1.0/rand')
def get_rand():
    db = get_db()
    cur = db.execute('select * from fortunes')
    count = cur.rowcount
    rand_id = random.randrange(0,count)
    return jsonify({'fortunes': fortunes[rand_id]})

@app.route('/fortunes/api/v1.0/count')
def get_count():
    db = get_db()
    cur = db.execute('select conunt(*) from fortunes')

# @app.route('/gulfort/api/v1.0/count')
# def get_count():


if __name__ == '__main__':
    app.run(debug = True)