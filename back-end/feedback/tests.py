import json

from django.test import TestCase

from .models import Question


def json_data(**data):
    return dict(
        data=json.dumps(data),
        content_type='application/json',
    )


class TestFeedback(TestCase):
    def setUp(self):
        Question.objects.create(
            key="thumbs",
            type="thumbs",
            choice_text="How are you feeling?",
            with_comment=True,
            comment_text="Do you want to provide additional comments?",
        )

    def assertOk(self, response):
        self.assertEqual(
            response.status_code, 200,
            f"Expected HTTP 200, got {response.status_code}. "
            f"Body: {response.content.decode('utf-8')}")

    def assertCount(self, total):
        answers = self.client.get('/question/thumbs/answer').json()
        self.assertEqual(len(answers), total)

    def assertSummary(self, positive, negative, empty):
        summary = self.client.get('/question/thumbs/summary').json()
        self.assertEqual(summary['values']['1'], positive)
        self.assertEqual(summary['values']['-1'], negative)
        self.assertEqual(summary['values'][''], empty)

    def test_submit_and_summary(self):
        self.assertCount(0)

        for value in [1, -1, 1, -1]:
            response = self.client.post(
                '/question/thumbs/answer',
                **json_data(value=value, submit=True))
            self.assertOk(response)

        self.assertCount(4)
        self.assertSummary(2, 2, 0)

        id_ = response.json()['id']

        response = self.client.patch(
            f'/answer/{id_}',
            **json_data(value=1, submit=True))
        self.assertOk(response)

        self.assertCount(4)
        self.assertSummary(3, 1, 0)

        response = self.client.post(
            '/question/thumbs/answer',
            **json_data())
        self.assertOk(response)

        self.assertCount(5)
        self.assertSummary(3, 1, 1)
