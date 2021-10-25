import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://naomiradke@localhost:5432/fyyur'

# Print SQL querion on the terminal
SQLALCHEMY_ECHO = True

# Disable track modification to avoid overhead
SQLALCHEMY_TRACK_MODIFICATIONS = False