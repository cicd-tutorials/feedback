from dataclasses import dataclass
from datetime import datetime
import uuid

from django.core.validators import RegexValidator
from django.db import models


@dataclass
class Choice:
    value: int
    label: str
    title: str

    @property
    def json(self):
        return dict(
            value=self.value,
            label=self.label,
            title=self.title,
        )


@dataclass
class Type:
    choices: list[Choice]

    @property
    def json(self):
        return dict(
            choices=[c.json for c in self.choices],
        )


TYPES = dict(
    thumbs=Type(choices=[
        Choice(value=-1, label="👎", title="Thumbs down"),
        Choice(value=1, label="👍", title="Thumbs up"),
    ]),
    weather=Type(choices=[
        Choice(value=-2, label="⛈️", title="Stormy"),
        Choice(value=-1, label="🌧️", title="Rainy"),
        Choice(value=0, label="☁️", title="Cloudy"),
        Choice(value=1, label="⛅", title="Partially sunny"),
        Choice(value=2, label="☀️", title="Sunny"),
    ]),
)


key_validator = RegexValidator(
    r"^[a-z0-9._-]+$",
    "Question key must only contain lowercase alphanumeric characters and "
    "hyphens.")


class Question(models.Model):
    key = models.CharField(
        max_length=64,
        primary_key=True,
        editable=False,
        validators=[key_validator])
    type = models.CharField()

    choice_text = models.CharField(max_length=512)
    with_comment = models.BooleanField(default=False)
    comment_text = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return f'{self.choice_text} (type={self.type}, key={self.key})'

    @property
    def json(self):
        data = dict(
            key=self.key,
            type=self.type,
            choice_text=self.choice_text,
            with_comment=self.with_comment,
            comment_text=self.comment_text,
        )
        if self.type in TYPES:
            data = {**data, **TYPES[self.type].json}
        return data


def _timestamp(timestamp: datetime | None) -> str | None:
    return timestamp.isoformat() if timestamp else None


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True)
    comment = models.TextField(max_length=512, blank=True, null=True)
    reference = models.CharField(max_length=64, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return (
            f'{self.id} (type={self.question.type}, key={self.question.key})')

    @property
    def json(self):
        return dict(
            id=self.id,
            key=self.question.key,
            value=self.value,
            comment=self.comment,
            reference=self.reference,
            created_at=_timestamp(self.created_at),
            updated_at=_timestamp(self.updated_at),
            submitted_at=_timestamp(self.submitted_at),
        )
