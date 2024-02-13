from django.contrib import admin

# Register your models here.
from django.contrib import admin
from judge.models import Assignment, TestCase, Question, Submission

from nested_admin import nested


class TestCaseAdminInlier(nested.NestedTabularInline):
    model = TestCase
    

class QuestionAdminInlier(nested.NestedTabularInline):
    extra = 1
    model =  Question
    readonly_fields = ('question_id', )
    inlines = (TestCaseAdminInlier, )


class AssignmentAdmin(nested.NestedModelAdmin):
    inlines = (QuestionAdminInlier,)



class QuestionAdmin(admin.ModelAdmin):
    model = Question
    readonly_fields = ('question_id', )
    inlines = (TestCaseAdminInlier, )
    

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Question, QuestionAdmin)
