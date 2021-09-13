# Generated by Django 3.2.5 on 2021-09-09 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aesci_api', '0006_remove_assignment_coderesult'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndicatorMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeMeasure', models.BigIntegerField(choices=[('1', 'Beginner'), ('2', 'Apprentice'), ('3', 'Competent'), ('4', 'Expert')], max_length=1)),
                ('description', models.CharField(max_length=60)),
                ('performanceIndicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.performanceindicator')),
            ],
        ),
    ]
