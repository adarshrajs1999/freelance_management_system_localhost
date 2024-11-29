# Generated by Django 5.0.2 on 2024-11-29 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers_app', '0015_rename_title_customer_task_work_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer_task',
            name='is_approved',
        ),
        migrations.RemoveField(
            model_name='customer_task',
            name='is_completed',
        ),
        migrations.AlterField(
            model_name='customer_task',
            name='work_category',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]