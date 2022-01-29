from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "nothing_secret_about_this"

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    return app
