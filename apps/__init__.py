from flask import Flask, jsonify
from config import Config

def api_response(status,message,data):
    return jsonify({
        "status" : status,
        "message" : message,
        "data" : data
    })


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from apps.api import bp as api_bp
    app.register_blueprint(api_bp,url_prefix='/api')
    
    return app


