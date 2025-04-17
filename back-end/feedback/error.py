from django.forms import ModelForm


class FeedbackError(Exception):
    def __init__(self, title: str, status: int = 500, errors=None):
        super().__init__(title)
        self.message = title
        self.status = status
        self.errors = errors

    @property
    def json(self):
        data = dict(
            title=self.message,
            status=self.status,
        )

        if self.errors is not None:
            data["errors"] = self.errors

        return data


class FormValidationFailed(FeedbackError):
    def __init__(self, form: ModelForm):
        try:
            resource = form.instance.__class__.__name__
        except AttributeError:
            resource = "Form"

        super().__init__(
            f"{resource} validation failed.",
            400,
            errors=form.errors.get_json_data(),
        )
