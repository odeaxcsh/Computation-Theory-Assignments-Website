from django.contrib import admin

# Register your models here.
from django.contrib import admin
from judge.models import Assignment, TestCase, Question


class TestCaseAdminInlier(admin.TabularInline):
    model = TestCase
    

class QuestionAdminInlier(admin.StackedInline):
    extra = 0
    model =  Question
    readonly_fields  = ('question_id', )
    fields = [('question_id', 'type', 'score')]
    exclude = ('description',)
    show_change_link = True


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']
    list_display_links = ['name']
    inlines = (QuestionAdminInlier, )


class QuestionAdmin(admin.ModelAdmin):
    list_filter = ['assignment']
    fields = [('assignment', 'type', 'score'), 'description']
    list_display = ('__str__', 'type', 'score', )
    list_display_links = ('__str__', )

    exclude = ('question_id', )
    inlines = (TestCaseAdminInlier, )

    ordering = ('-assignment', 'created_at')    

    
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Question, QuestionAdmin)
