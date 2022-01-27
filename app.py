import logging
from hashlib import md5

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask.logging import default_handler
app = Flask("app")
app.logger.setLevel(logging.DEBUG)
app.logger.propagate = False
default_handler.setFormatter(logging.Formatter('[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(message)s'))

app.config.from_pyfile("default_config.py")
app.config.from_envvar("APP_SETTINGS", silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))


@app.route("/")
def index():
    users = User.query.all()
    app.logger.info("info")
    app.logger.debug("debug")
    app.logger.error("error")
    response = {
        "total": len(users),
        "users": [{"username": user.username} for user in users],
        "secret": app.config['SUPERSECRET_INFO']
    }
    return jsonify(response)


@app.route("/api/register", methods=["POST"])
def register():
    user_data = request.json
    if not user_data or "username" not in user_data or "password" not in user_data:
        return jsonify({"error": "invalid_request"}), 400

    try:
        user = User(
            username=user_data["username"],
            password=md5(user_data["password"].encode()).hexdigest(),
        )
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "already_exists"}), 400

    return jsonify({"username": user.username}), 200

#
# from logging_tree import printout
# printout()