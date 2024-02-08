from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD


class Assignment(models.Model):
    name = models.CharField(max_length=100)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Question(models.Model):
    class QuestionTypes(models.TextChoices):
        DFA = "DFA", _("DFA")
        NFA = "NFA", _("NFA")
        PDA = "PDA", _("PDA")


    series_id = models.ForeignKey(to=Assignment, on_delete=models.CASCADE, related_name='questions')
    question_id = models.IntegerField(null=True)
    description = MarkdownField(
        rendered_field='description_rendered', 
        validator=VALIDATOR_STANDARD, use_editor=False, use_admin_editor=True
    )
    description_rendered = RenderedMarkdownField()



    type = models.CharField(
        max_length=3,
        choices=QuestionTypes.choices,
        default=QuestionTypes.DFA
    )

    score = models.IntegerField()


    def save(self, *args, **kwargs):
        if self._state.adding:
            self.question_id = self.series_id.questions.count()
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.description


class TestCase(models.Model):
    question_id = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name='tests')
    test = models.CharField(max_length=100)
    accept_or_reject = models.BooleanField()
    show = models.BooleanField()

    def __str__(self) -> str:
        return self.test



class Submission(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE, related_name='submissions')
    datetime = models.DateTimeField(auto_now_add=True)
    machine = models.JSONField()
    result = models.IntegerField()
