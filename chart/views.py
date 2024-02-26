from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


from django.http import Http404, HttpResponse
from judge.models import Assignment, Submission

from django.db.models import F, Case, When, Value, IntegerField
from django.db.models import OuterRef
from django.db.models.functions import DenseRank
from django.db.models import Window, F

# Create your views here.

from django.utils import timezone
from datetime import timedelta


@login_required
def home(request):
    assignments = Assignment.objects.all()

    now = timezone.now()
    assignments = assignments.filter(start_date__lt=now).annotate(
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

    now = timezone.now()
    if assignment.start_date >= now:
        return Http404()
    

    active = assignment.end_date >= now
    
    submissions = Submission.objects.filter(user=user, question__in=OuterRef('pk')).order_by('-datetime')[:1]
    questions = assignment.questions.all().annotate(
        result=submissions.values('result')
    )

    results = questions.values_list('score', 'result')

    result = sum([score * submission / 100 if submission else 0 for score, submission in results])
    all_scores = sum([score for score, _ in results])

    return render(request, 'assignment.html', context={
        'assignment': assignment, 
        'questions': questions, 
        'active': active,
        'score': result,
        'all_scores': all_scores
    })

