# Generated by Django 4.2.5 on 2024-02-10 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_app", "0002_course"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="course_instructor",
            field=models.CharField(default="high", max_length=255),
            preserve_default=False,
        ),
    ]