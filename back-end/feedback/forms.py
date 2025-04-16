from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Answer, TYPES


class CreateAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['question','reference', 'value', 'comment']


class ModifyAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['value', 'comment']

    def clean_value(self):
        q = self.instance.question
        t = TYPES.get(q.type)
        if t is None:
            raise ValidationError(
                "Invalid question type: "
                f"expected one of {list(TYPES.keys())}, got {q.type}")

        expected = [i.value for i in t.choices]
        value = self.cleaned_data['value']
        if value not in expected:
            raise ValidationError(
                f"Invalid value: expected one of {expected}, got {value}")

        return value
