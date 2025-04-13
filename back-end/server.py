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
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('FEEDBACK_DB_URL', 'sqlite:///server.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@dataclass
class FeedbackQuestion(db.Model):
    key: str
    text: str
    type: str
    with_comment: bool

    key = db.Column(db.String(64), primary_key=True)
    text = db.Column(db.String(512))
    type = db.Column(db.String(16))
    with_comment = db.Column(db.Boolean())

    @property
    def json(self):
        return dict(
            key=self.key,
            text=self.text,
            type=self.type,
            with_comment=self.with_comment,
        )


def _timestamp(input: datetime | None) -> str | None:
    if input is None:
        return None
    return f'{input.isoformat()}Z'


@dataclass
class FeedbackAnswer(db.Model):
    id: str
    key: str
    value: int
    comment: str
    group: str
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime

    id = db.Column(db.String(36), primary_key=True)
    key = db.Column(db.String(64))
    value = db.Column(db.Integer())
    comment = db.Column(db.String(512))
    group = db.Column(db.String(32))
    created_at = db.Column(db.DateTime())
    updated_at = db.Column(db.DateTime())
    submitted_at = db.Column(db.DateTime())

    @property
    def json(self):
        return dict(
            id=self.id,
            key=self.key,
            value=self.value,
            comment=self.comment,
            group=self.group,
            created_at=_timestamp(self.created_at),
            updated_at=_timestamp(self.updated_at),
            submitted_at=_timestamp(self.submitted_at),
        )


# Create table if it does not exist
for _ in range(5):
    try:
        with app.app_context():
            db.create_all()

            # TODO: Check if the table is empty
            db.session.add(FeedbackQuestion(
                key="how-are-you-feeling",
                text="How are you feeling?",
                type="thumbs",
                with_comment=False,
            ))
            db.session.commit()
    except BaseException:
        sleep(2)


def get_feedback(key: str):
    q = db.session.query(FeedbackQuestion).filter(FeedbackQuestion.key == key).one_or_none()
    if q is None:
        return dict(error="Question not found"), 404
    return jsonify(q.json), 200


def get_answers(key: str):
    q = db.session.query(FeedbackQuestion).filter(FeedbackQuestion.key == key).one_or_none()
    if q is None:
        return dict(error="Question not found"), 404

    rows = db.session.execute(db.select(FeedbackAnswer).where(FeedbackAnswer.key == key)).all()
    return jsonify([row.FeedbackAnswer.json for row in rows]), 200


def post_answer(key: str, input):
    q = db.session.query(FeedbackQuestion).filter(FeedbackQuestion.key == key).one_or_none()
    if q is None:
        return dict(error="Question not found"), 404

    id_ = str(uuid4())

    submitted_at = None
    if input.get("submit") == True:
        submitted_at = datetime.utcnow()

    # TODO: validate input
    db.session.add(FeedbackAnswer(
        id=id_,
        key=key,
        value=input.get("value"),
        created_at=datetime.utcnow(),
        submitted_at=submitted_at,
    ))
    db.session.commit()

    return dict(id=id_), 200


def get_feedback_summary(key: str):
    q = db.session.query(FeedbackQuestion).filter(FeedbackQuestion.key == key).one_or_none()
    if q is None:
        return dict(error="Question not found"), 404

    rows = db.session.execute(
        db.select(
            func.count(
                FeedbackAnswer.id),
            FeedbackAnswer.value).where(FeedbackAnswer.key == key).group_by(
            FeedbackAnswer.value)).all()

    data = dict()
    if q.type == "thumbs":
        values = dict(positive=0, negative=0)
        for count, value in rows:
            if value == 1:
                values["positive"] = count
            elif value == -1:
                values["negative"] = count
        data["values"] = values

    return jsonify(data), 200


@app.route("/feedback/<string:key>/answer", methods=['GET', 'POST'])
def answer(key: str):
    if request.method == "POST":
        return post_answer(key, request.json)
    return get_answers(key)


@app.route("/feedback/<string:key>", methods=['GET'])
def feedback(key: str):
    return get_feedback(key)


@app.route("/feedback/<string:key>/summary", methods=['GET'])
def feedback_summary(key: str):
    return get_feedback_summary(key)
