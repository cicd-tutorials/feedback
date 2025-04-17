from django.core.management.base import BaseCommand

from feedback.models import Question

QUESTIONS = [
    dict(
        key="thumbs",
        type="thumbs",
        choice_text="How are you feeling?",
        with_comment=True,
        comment_text="Do you want to provide additional comments?",
    ),
    dict(
        key="weather",
        type="weather",
        choice_text="How is the weather?",
        with_comment=True,
        comment_text="Do you want to provide additional details?",
    ),
]


class Command(BaseCommand):
    help = "Create demo questions."

    def handle(self, *args, **options):
        for q in QUESTIONS:
            key = q.get('key')
            # Check if the question already exists
            if not Question.objects.filter(key=key).exists():
                Question.objects.create(**q)
                self.stdout.write(
                    self.style.SUCCESS(f"Question '{key}' created.")
                )
            else:
                self.stdout.write(
                    self.style.NOTICE(
                        f"Question '{key}' already exists, skipping."
                    )
                )
