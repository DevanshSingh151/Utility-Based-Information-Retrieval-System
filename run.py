import os
from flask import render_template
from app import create_app

app = create_app()

@app.route('/')
def serve_index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") == "development"
    app.run(host='0.0.0.0', port=port, debug=debug)
