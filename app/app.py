import threading
import uuid
import flask_cors

from flask import Flask, Blueprint
from flask_restx import Api

from database.factory import DatabaseFactory

from controller.user_controller import api as user_ns
from controller.auth_controller import api as auth_ns

from config.config import Config

# Create Blueprint
blueprint = Blueprint(name="v1", import_name=__name__, url_prefix="/")

# Setting Bearer Authorization
authorizations = {
    "Bearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
    }
}

# Create API
api_v1 = Api(
    blueprint,  # or flask app instance
    version="1",
    title="flask-restx-boilerplate API Server",
    description="flask-restx-boilerplate API Document",
    contact="inseok.seoo@gmail.com",
    prefix="/api",
    authorizations=authorizations,
    security="Bearer",
)


def create_app():  # pragma: no cover
    _app = Flask(__name__)

    # Setting application config
    _app.config["RESTX_MASK_SWAGGER"] = Config.RESTX_MASK_SWAGGER

    @_app.before_request
    def pre_request():  # pylint: disable=unused-variable
        uuid4 = uuid.uuid4()
        thread = threading.current_thread()
        thread.request_id = uuid4
        print(uuid4)

    with _app.app_context():
        # Init database
        DatabaseFactory.initialize(_app)

        # Setting cors
        flask_cors.CORS(
            _app, resources={r"*": {"origins": "*"}}
        )  # == flask_cors.CORS(_app)

        # Adding namespace
        api_v1.add_namespace(user_ns, "/")
        api_v1.add_namespace(auth_ns, "/")

        _app.register_blueprint(blueprint)

    return _app


app = create_app()

if __name__ == "__main__":  # pragma: no cover
    app.run(
        host="0.0.0.0", use_reloader=False, use_debugger=False, threaded=True
    )
