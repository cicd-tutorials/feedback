from flask import Flask, request

app = Flask(__name__)

data = dict(positive=0, negative=0)


def get_feedback():
    return data


def post_feedback(input):
    if input["type"] == "positive":
        data['positive'] += 1
    if input["type"] == "negative":
        data['negative'] += 1


@app.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        post_feedback(request.json)
        return '', 204
    return get_feedback(), 200
