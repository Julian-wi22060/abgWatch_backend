from flask import Flask
from helper.v_candidacy_mandates import v_cm_bp


def create_app():
    app = Flask(__name__)

    # register blueprints
    app.register_blueprint(v_cm_bp, url_prefix="/v_candidacy_mandates")

    @app.route("/")
    def index():
        return "AbgWatch Backend API läuft!"
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=50555, debug=True)
