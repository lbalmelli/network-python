"""
	The script above simply creates the application object as an instance 
	of class Flask imported from the flask package.

"""
from flask import Flask

# __name__ variable passed to the Flask class is a Python predefined 
# variable, which is set to the name of the module in which it is used.
app = Flask(__name__)

# The bottom import is a workaround to circular imports, a common problem 
# with Flask applications. You are going to see that the routes module 
# needs to import the app variable defined in this script, so putting one 
# of the reciprocal imports at the bottom avoids the error that results 
# from the mutual references between these two files.

from app import routes

# The routes are the different URLs (end-points) that the application implements. 