# Generated by Django 3.2.8 on 2021-10-22 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0010_alter_assignmentstudent_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationResult',
            fields=[
                ('codeResult', models.IntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
        migrations.RemoveField(
            model_name='assignmentstudent',
            name='grade',
        ),
        migrations.AddField(
            model_name='evaluationassignment',
            name='grade',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='carrer',
            field=models.CharField(max_length=60),
        ),
    ]