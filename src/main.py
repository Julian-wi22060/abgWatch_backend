from flask import Flask
from helper.v_candidacy_mandates import v_cm_bp
from helper.vote_poll_details import vote_poll


def create_app():
    """
    Creates and configures the Flask application.
    Features:
        - Registers the blueprints for the API endpoints.
        - Provides a health check endpoint at `/health`.
    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Register blueprints for each API
    app.register_blueprint(v_cm_bp, url_prefix="/v_candidacy_mandates")
    app.register_blueprint(vote_poll, url_prefix="/vote_poll_details")

    # Health-endpoint
    @app.route("/health")
    def index():
        """
        Health-check endpoint to verify the API's operational status.
        Returns:
            str: A confirmation message that the API is healthy.
        """
        return "Backend API healthy!"
    return app


if __name__ == "__main__":
    """
    Entry point for running the Flask application.
    Starts the application on host `0.0.0.0` and port `50555` with debug mode enabled.
    """
    app = create_app()
    app.run(host="0.0.0.0", port=50555, debug=True)
