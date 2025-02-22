from flask import Flask
from routes.auth import auth
from routes.movie import movie
from routes.event import event
from routes.booking import booking
from routes.user import user
from routes.general import general
from routes.database import db
from routes.chatbot import chatbot



def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object('config.DevelopmentConfig')
    
    # Register Blueprints
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(movie, url_prefix='/')
    app.register_blueprint(event, url_prefix='/')
    app.register_blueprint(booking, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(general, url_prefix='/')
    app.register_blueprint(chatbot)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='127.0.0.1', port=5000)