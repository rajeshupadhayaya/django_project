# Generated by Django 2.2.1 on 2020-01-05 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_exam_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_pic',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
