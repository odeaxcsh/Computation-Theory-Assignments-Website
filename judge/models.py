from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD
from django.utils.functional import cached_property


class Assignment(models.Model):
    name = models.CharField(max_length=100)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Question(models.Model):
    readonly_fields = ('question_id', 'created_at')
    class QuestionTypes(models.TextChoices):
        DFA = "DFA", _("DFA")
        NFA = "NFA", _("NFA")
        PDA = "PDA", _("PDA")


    assignment = models.ForeignKey(to=Assignment, on_delete=models.CASCADE, related_name='questions')
    description = MarkdownField(
        rendered_field='description_rendered', 
        validator=VALIDATOR_STANDARD, use_editor=False, use_admin_editor=True, blank=True
    )
    description_rendered = RenderedMarkdownField()

    created_at = models.DateTimeField(auto_now_add=True)

    type = models.CharField(
        max_length=3,
        choices=QuestionTypes.choices,
        default=QuestionTypes.DFA
    )

    score = models.IntegerField()


    @cached_property
    def question_id(self):
        return self.assignment.questions.filter(created_at__lt=self.created_at).count() + 1
    
    def __str__(self) -> str:
        return f'{self.assignment.name}. Q-{self.question_id}'


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

