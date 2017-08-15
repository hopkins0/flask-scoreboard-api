from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from flask import current_app
from flask import request
import json
from copy import copy, deepcopy
import requests
import os



@main.route('/', methods=['GET', 'POST'])
def index():
	with current_app.test_client() as client:
		resp = client.get(url_for('main.api_10_contest_activo_info'))
		data = json.loads(resp.data)
	return render_template('index.html', info=data)
