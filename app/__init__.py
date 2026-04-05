from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    with app.app_context():
        from app.routes import main_routes
        app.register_blueprint(main_routes.bp)
        
    return app
