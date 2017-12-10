import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/jbv2/")

from jbv2 import app as application
application.secret_key = "Don't panic!"
