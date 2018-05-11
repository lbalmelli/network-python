"""

	View function: handler for the route

"""
from app import app

# the @app.route decorator creates an association between the URL given as an 
# argument and the function.
# These decorators associate the URLs / and /index to this function. 
@app.route('/')
@app.route('/index')
def index():
	"""
		This view function just returns a greeting as a string.
	"""
	return "Hello, World!"
