from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from judge.models import Assignment, Submission

from django.db.models import F, Case, When, Value, IntegerField
from django.db.models import OuterRef, Subquery

# Create your views here.

from django.utils import timezone
from datetime import timedelta


@login_required
def home(request):
    assignments = Assignment.objects.all()

    now = timezone.now()
    assignments = assignments.annotate(
        remained=(F('end_date') - now),
        active=Case(
            When(remained__gt=timedelta(), then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
        )
    )

    return render(request, 'home.html', context={'assignments': assignments})


@login_required
def assignment(request, assignment_id):
    user = request.user

    assignment = get_object_or_404(Assignment, pk=assignment_id)
    
    
    submissions = Submission.objects.filter(user=user, question__in=OuterRef('pk'))
    submissions = assignment.questions.all().annotate(
        last_submission=submissions.order_by('datetime').values("result")[:1]
    )

    submissions = dict(submissions.values_list('question_id', 'last_submission'))
    return render(request, 'assignment.html', context={'assignment': assignment, 'submissions': submissions})

