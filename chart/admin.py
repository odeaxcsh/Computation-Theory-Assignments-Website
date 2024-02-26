from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SubmissionSummary


@admin.register(SubmissionSummary)
class SubmissionSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/submission_summary_change_list.html'
    date_hierarchy = 'datetime'
