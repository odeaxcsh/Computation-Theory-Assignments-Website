from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.http import HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404
from .models import Question, Assignment, Submission
from datetime import datetime

import json
from .judge import run



@login_required
def viewer(request):
    return render(request, 'judge.html')
        


@login_required
def index(request, assignment, question):
    user = request.user

    assignment = get_object_or_404(Assignment, pk=assignment)
    question = get_object_or_404(assignment.questions, pk=question)

    last_submission = Submission.objects.filter(user=user, question=question).order_by('-datetime')

    if last_submission.count():
        last_submission = last_submission[0]
        last_submission.machine = json.dumps(last_submission.machine)

    else:
        last_submission = None
        
    if request.method == 'GET':
        return render(request, 'judge.html', context={
            'assignment': assignment,
            'question': question,
            'last_submission': last_submission
        })
    

    elif request.method == 'POST':
        body = request.body.decode('utf-8')
        if len(body) > 1024 * 1024 * 1:
            return JsonResponse(content='Fuck you piece of shit; hack your mother')
        
        if last_submission and (timezone.now() - last_submission.datetime).total_seconds() < 10:
            time_passed = (timezone.now() - last_submission.datetime).total_seconds()
            message = f'''
                Calm the fuck down
                I'm not paied enough for this
                Try again in {round(10 - time_passed)} seconds
            '''
            return JsonResponse({
                'wait': round(10 - time_passed), 
                'message': message.format(),
            })

        machine = json.loads(body)
        tests = question.tests.values_list('test')
        if machine['type'] != question.type:
            message = f'You should draw a {question.type}'
            result = 0
        else:
            try:
                results = run(machine, tests)
                expecteds = question.tests.values_list('accept_or_reject')

                outcome = [result == expected[0] for result, expected in zip(results, expecteds)]
                if len(outcome) == 0:
                    result = 0
                    message = f'No test cases'
                else:
                    result = round(sum(outcome) / len(outcome) * 100)
                    message = f'Your machine passed {result}% of tests'

            except Exception as e:
                message = f'Your machine is not defined properly: {e}'
                result = 0
        
        submission = Submission(machine=machine, question=question, result=result, user=user)
        submission.save()

        date = datetime.strftime(submission.datetime, "%b. %d, %Y %I:%M %p")
        return JsonResponse({
            'message': message,
            'submission': {
                'datetime': date,
                'result': submission.result
            }
        })

        