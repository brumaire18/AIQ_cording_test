from flask import Flask
from config import Config
from app.models import db
from app.blueprints import blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    for bp, url_prefix in blueprints:
        app.register_blueprint(bp, url_prefix=url_prefix)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
