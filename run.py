import os
import sys

# Ensure module visibility
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app
from app.config import FLASK_ENV

app = create_app()

if __name__ == '__main__':
    print(f"🚀 Booting Flask App on http://localhost:5000 (Env: {FLASK_ENV})")
    debug_mode = (FLASK_ENV == 'development')
    app.run(host='0.0.0.0', port=5000, debug=debug_mode, use_reloader=False)
