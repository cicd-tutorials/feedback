from dataclasses import dataclass
from datetime import datetime
from os import getenv
from time import sleep
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_URL', 'sqlite:///server.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@dataclass
class FeedbackItem(db.Model):
    id: str
    type: str
    timestamp: datetime

    id = db.Column(db.String(36), primary_key=True)
    type = db.Column(db.String(8))
    timestamp = db.Column(db.DateTime())

    @property
    def json(self):
        return dict(
            id=self.id,
            type=self.type,
            timestamp=f'{self.timestamp.isoformat()}Z')


# Create table if it does not exist
for _ in range(5):
    try:
        with app.app_context():
            db.create_all()
    except BaseException:
        sleep(2)


def get_feedback():
    rows = db.session.execute(db.select(FeedbackItem)).all()
    return jsonify([row.FeedbackItem.json for row in rows])


def post_feedback(input):
    id_ = str(uuid4())

    db.session.add(FeedbackItem(
        id=id_,
        type=input["type"],
        timestamp=datetime.utcnow()
    ))
    db.session.commit()

    return dict(id=id_)


def get_feedback_summary():
    rows = db.session.execute(
        db.select(
            func.count(
                FeedbackItem.id),
            FeedbackItem.type).group_by(
            FeedbackItem.type)).all()

    data = dict(positive=0, negative=0)
    for count, type_ in rows:
        data[type_] = count

    return jsonify(data)


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        return post_feedback(request.json), 200
    return get_feedback(), 200


@app.route("/feedback/summary", methods=['GET'])
def feedback_summary():
    return get_feedback_summary(), 200
