import sys
import logging
 
sys.path.insert(0, '/var/www/skol')
sys.path.insert(0, '/var/www/skol/venv/lib/python3.9/site-packages/')
 
# Set up logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
 
# Import and run the Flask app
from skol import app as application
