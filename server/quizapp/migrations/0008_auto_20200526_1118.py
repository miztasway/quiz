# Generated by Django 3.0.6 on 2020-05-26 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0007_auto_20200526_1051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('date',)},
        ),
        migrations.AlterField(
            model_name='quiz',
            name='pass_mark',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='score_for_each_question',
            field=models.FloatField(),
        ),
    ]
