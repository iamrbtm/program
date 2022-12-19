import sys
project_home = u'/home/onlymyli/public_html/dudefishprinting'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
from printing import create_app
application = create_app()