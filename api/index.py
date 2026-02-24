import sys
import os

# Add the deeptrace_backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'deeptrace_backend'))

from deeptrace_backend.app import app

# Export the app for Vercel
export = app
