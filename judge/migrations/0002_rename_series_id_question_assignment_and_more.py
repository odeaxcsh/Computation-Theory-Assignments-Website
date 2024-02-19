# Generated by Django 4.2.10 on 2024-02-19 23:13

from django.db import migrations, models
import django.utils.timezone
import markdownfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='series_id',
            new_name='assignment',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_id',
        ),
        migrations.AddField(
            model_name='question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='description',
            field=markdownfield.models.MarkdownField(blank=True, rendered_field='description_rendered', use_editor=False),
        ),
    ]