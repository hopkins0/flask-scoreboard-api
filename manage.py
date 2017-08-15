#!/usr/bin/env python
import os
from app import create_app
import logging
from logging.handlers import RotatingFileHandler
from flask_script import Manager, Shell



app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Create the logger file
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)



# Create the manager from app
manager = Manager(app)

def make_shell_context():
	return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
	manager.run()