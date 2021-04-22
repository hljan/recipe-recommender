from flask import Flask
from .models import PyNeoGraph

def create_app():
    app = Flask(__name__)
    app.secret_key = 'd1255677-af1b-4c77-a981-7e8b1d89ff99'
    
    # route config
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .text_search import textSearch as text_search_blueprint
    app.register_blueprint(text_search_blueprint)
    from .visual_search import visualSearch as visual_search_blueprint
    app.register_blueprint(visual_search_blueprint)

    return app


# run flask app
if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=5020, debug=True)
