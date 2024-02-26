from django.http import HttpResponse
import xlwt

from django.contrib import admin
from django.contrib.auth.models import User

import re

from django.forms import ModelForm
from judge.models import Assignment, TestCase, Question, Submission



class TestCaseAdminInlier(admin.TabularInline):
    model = TestCase
    

class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        return not self.instance.pk or super().has_changed()
    

class QuestionAdminInlier(admin.StackedInline):
    extra = 0
    model =  Question
    readonly_fields  = ('question_id', )
    fields = [('question_id', 'type', 'score')]
    exclude = ('description',)
    show_change_link = True
    form = AlwaysChangedModelForm


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']
    list_display_links = ['name']
    inlines = (QuestionAdminInlier, )

    actions = ["export_to_csv"]

    @admin.action(description="Export Selected Assignemnts")
    def export_to_csv(self, request, assignments):
        book = xlwt.Workbook()
        pks = [str(pk) for pk, in assignments.values_list('pk')]

        for assignment in assignments:
            sheet = book.add_sheet(re.sub('\W+','', assignment.name))

            for question in assignment.questions.all():
                sheet.write(0, question.question_id, f'Q-{question.question_id}/{question.score}')
            sheet.write(0, assignment.questions.count() + 1, 'Sum')

            for i, user in enumerate(User.objects.all(), 1):
                sheet.write(i, 0, user.username)

                score = 0
                for question in assignment.questions.all():
                    submission = Submission.objects.filter(user=user, question=question)
                    if submission.count() > 0:
                        submission = submission.latest('datetime')
                        sheet.write(i, question.question_id, submission.result)
                        score += submission.result * question.score
                sheet.write(i, assignment.questions.count() + 1, score / 100)
        
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'''attachment; filename="assignments-{'-'.join(pks)}.xls"'''},
        )
        book.save(response)
        return response


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['assignment']
    fields = [('assignment', 'type', 'score'), 'description']
    list_display = ('__str__', 'type', 'score', )
    list_display_links = ('__str__', )
    list_filter = ['assignment']

    exclude = ('question_id', )
    inlines = (TestCaseAdminInlier, )

    ordering = ('-assignment', 'created_at')
    
    def has_module_permission(self, request):
        return False
    

    
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Question, QuestionAdmin)
