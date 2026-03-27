import sys
import os

# Add the root directory so we can import 'deeptrace_backend'
# And add 'deeptrace_backend' itself for inner imports like 'crypto.aes'
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
backend = os.path.join(root, 'deeptrace_backend')

if root not in sys.path: sys.path.insert(0, root)
if backend not in sys.path: sys.path.insert(0, backend)

try:
    from deeptrace_backend.app import app
except Exception as e:
    import traceback
    from flask import Flask, jsonify
    app = Flask(__name__)
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return jsonify({
            "error": "Initialization Error",
            "message": str(e),
            "traceback": traceback.format_exc(),
            "sys_path": sys.path,
            "cwd": os.getcwd()
        }), 500
