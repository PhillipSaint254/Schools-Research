# Generated by Django 4.1.7 on 2023-05-19 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0003_remove_schoolsinfrastructurestatus_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="schoolsinfrastructurestatus",
            name="teacher_email",
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
