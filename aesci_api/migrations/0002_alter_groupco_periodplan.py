# Generated by Django 3.2.8 on 2021-11-28 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupco',
            name='periodPlan',
            field=models.CharField(choices=[('2021-2', '2021-2S'), ('2022-1', '2022-1S')], max_length=60),
        ),
    ]