
activate_this = '/home/abhishekbiswal/rg/site/flask/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.append("/home/abhishekbiswal/rg/site")

from app import app as application