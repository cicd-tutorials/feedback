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


class FeedbackException(Exception):
    def __init__(self, message: str, status: int = 500):
        super().__init__(message)
        self.message = message
        self.status = status

    @property
    def json(self):
        return dict(
            error=self.message,
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


def get_question(key: str):
    q = db.session.query(FeedbackQuestion).filter(FeedbackQuestion.key == key).one_or_none()
    if q is None:
        raise FeedbackException("Question not found", 404)
    return q


def get_feedback(key: str):
    return jsonify(get_question(key).json), 200


def get_answers(key: str):
    get_question(key)

    rows = db.session.execute(db.select(FeedbackAnswer).where(FeedbackAnswer.key == key)).all()
    return jsonify([row.FeedbackAnswer.json for row in rows]), 200


def validate_value(q: FeedbackQuestion, value: int):
    if q.type == "thumbs":
        if value not in [-1, 1]:
            raise FeedbackException("Invalid value", 400)


def update_answer(key: str, id_: str, input) -> FeedbackAnswer:
    q = get_question(key)

    if id_ is None:
        id_ = str(uuid4())
        a = FeedbackAnswer(
            id=id_,
            key=key,
            created_at=datetime.utcnow(),
        )
    else:
        a = db.session.query(FeedbackAnswer).filter(FeedbackAnswer.id == id_).one_or_none()
        if a is None:
            raise FeedbackException("Answer not found", 404)
        if a.key != key:
            raise FeedbackException("Answer does not belong to given question", 400)
        a.updated_at = datetime.utcnow()

    if input.get("submit") == True:
        a.submitted_at = datetime.utcnow()

    if input.get("value") is not None:
        value = input.get("value")
        validate_value(q, value)
        a.value = input.get("value")

    if input.get("comment") is not None:
        a.comment = input.get("comment")

    if input.get("group") is not None:
        a.group = input.get("group")

    return a


def patch_answer(key: str, id_: str, input):
    a = update_answer(key, id_, input)
    db.session.commit()

    return dict(a.json), 200


def post_answer(key: str, input):
    a = update_answer(key, None, input)
    db.session.add(a)
    db.session.commit()

    return dict(a.json), 200


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


@app.route("/feedback/<string:key>", methods=['GET'])
def feedback(key: str):
    return get_feedback(key)


@app.route("/feedback/<string:key>/answer", methods=['GET', 'POST'])
def answers(key: str):
    if request.method == "POST":
        return post_answer(key, request.json)
    return get_answers(key)

@app.route("/feedback/<string:key>/answer/<string:id_>", methods=['PATCH'])
def answer(key: str, id_: str):
    if request.method == "PATCH":
        return patch_answer(key, id_, request.json)


@app.route("/feedback/<string:key>/summary", methods=['GET'])
def feedback_summary(key: str):
    return get_feedback_summary(key)


@app.errorhandler(FeedbackException)
def handle_app_error(e):
    return jsonify(e.json), e.status
