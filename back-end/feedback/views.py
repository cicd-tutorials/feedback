from datetime import datetime, timezone
import json

from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .error import FeedbackError, FormValidationFailed
from .forms import CreateAnswerForm, ModifyAnswerForm
from .models import Choice, Question, Answer, TYPES


def _feedback_error_as_json(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FeedbackError as e:
            return JsonResponse(e.json, status=e.status)
    return wrapper


def _get_question(key: str):
    try:
        q = Question.objects.get(key=key)
    except Question.DoesNotExist:
        raise FeedbackError("Question not found", 404)
    return q


def _parse_json_body(request: HttpRequest):
    try:
        return json.loads(request.body)
    except BaseException:
        raise FeedbackError(
            "Could not parse JSON data from request body.",
            400,
        )


@_feedback_error_as_json
def question(request: HttpRequest, key: str):
    if request.method != "GET":
        raise FeedbackError("Method not allowed", 405)
    return JsonResponse(_get_question(key).json)


def _get_answers(key: str):
    return JsonResponse([a.json for a in _get_question(key).answer_set.all()], safe=False)


def _post_answer(request: HttpRequest, key: str):
    q = _get_question(key)
    data = _parse_json_body(request)

    f = CreateAnswerForm({**data, 'question': q})
    if not f.is_valid():
        raise FormValidationFailed(f)

    return JsonResponse(f.save().json)


@_feedback_error_as_json
def question_answers(request: HttpRequest, key: str):
    if request.method == "POST":
        return _post_answer(request, key)
    elif request.method == "GET":
        return _get_answers(key)
    raise FeedbackError("Method not allowed", 405)


@_feedback_error_as_json
def answer(request: HttpRequest, id_: str):
    if request.method != "PATCH":
        raise FeedbackError("Method not allowed", 405)

    try:
        a = Answer.objects.get(id=id_)
    except Answer.DoesNotExist:
        raise FeedbackError("Answer not found", 404)

    data = _parse_json_body(request)
    if data.pop("submit", None):
        a.submitted_at = datetime.now(timezone.utc)

    f = ModifyAnswerForm({**a.json, **data}, instance=a)
    if not f.is_valid():
        raise FormValidationFailed(f)

    return JsonResponse(f.save().json)


def _value_to_str(value: int | None) -> str:
    if value is None:
        return ""
    if isinstance(value, Choice):
        return str(value.value)
    return str(value)


@_feedback_error_as_json
def summary(request: HttpRequest, key: str):
    if request.method != "GET":
        raise FeedbackError("Method not allowed", 405)

    q = _get_question(key)

    rows = q.answer_set.values("value").annotate(count=Count('*'))

    values = {}
    for c in TYPES.get(q.type).choices:
        values[_value_to_str(c)] = 0
    values[_value_to_str(None)] = 0

    total = 0
    non_null = 0
    for row in rows:
        count = row.get("count", 0)
        value = row.get("value", None)

        values[_value_to_str(value)] = count

        total += count
        if value is not None:
            non_null += count

    data = dict(
        count_non_null=non_null,
        count_total=total,
        values=values,
    )
    return JsonResponse(data)
