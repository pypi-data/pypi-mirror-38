__version__ = "0.6.1"

from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
from ccfilestore import CCFileStore


def create_app(test_config=None):
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
        print (app.config)
    else:
        # load the test config if passed in
        app.config['USERS'] = test_config['users']
        app.config['DBDIR'] = test_config['dbdir']

    users = app.config['USERS']
    dbdir = app.config['DBDIR']
    store = CCFileStore(dbdir)

    @auth.get_password
    def get_pw(username):
        if username in users:
            return users.get(username)
        return None

    @app.route('/<key>', methods=["GET", "HEAD"])
    def get(key):
        val = store.get(key)
        if val is not None:
            return val
        return "", 404

    @app.route('/<key>', methods=["PUT"])
    @auth.login_required
    def put(key):
        if len(key) < 32:
            return "key needs to be at least 32 chars long", 400
        if not key.isalnum():
            return "key {!r} needs to consist of alpha-numeric characters".format(key), 400
        value = store.get(key)
        if value is not None:
            if value == request.data:
                return "", 202
            else:
                return "", 409
        store.set_as(auth.username(), key, request.data)
        return ""

    @app.route('/<user>/', methods=["DELETE"])
    @auth.login_required
    def delete(user):
        if request.authorization['username'] != user:
            return repr(request.authorization["username"]) + " " + repr(user), 403
        store.delete_user(user)
        return ""

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
