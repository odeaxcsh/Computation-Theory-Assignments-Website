from django.db import models


from judge.models import Submission

class SubmissionSummary(Submission):
    class Meta:
        proxy = True
        verbose_name = 'Submission Summary'
        verbose_name_plural = 'Submission Summary'
