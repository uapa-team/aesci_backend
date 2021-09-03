# Generated by Django 3.2.5 on 2021-09-01 20:50

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('username', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('idPerson', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=60)),
                ('charge', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('idAssignment', models.AutoField(primary_key=True, serialize=False)),
                ('nameAssignament', models.CharField(max_length=60)),
                ('dateAssignment', models.DateTimeField(default=django.utils.timezone.now)),
                ('dateLimitAssignment', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='CoEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentAttached', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('codeCourse', models.BigIntegerField(default=1, primary_key=True, serialize=False)),
                ('referencePlan', models.IntegerField(default=1)),
                ('nameCourse', models.CharField(default='Test', max_length=60)),
                ('departmentCourse', models.CharField(default=1, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='GroupCo',
            fields=[
                ('numGroup', models.BigIntegerField(primary_key=True, serialize=False)),
                ('periodPlan', models.CharField(default='Test', max_length=60)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.course')),
            ],
        ),
        migrations.CreateModel(
            name='GroupStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.groupco')),
            ],
        ),
        migrations.CreateModel(
            name='HomeworkGroupStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.FloatField(default=None, null=True)),
                ('link', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(max_length=10), size=8), null=True, size=8)),
                ('idGroupStudent', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='aesci_api.groupstudent')),
                ('idHomework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.assignment')),
            ],
        ),
        migrations.CreateModel(
            name='PairEvaluator',
            fields=[
                ('username', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('idPerson', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=60)),
                ('institution', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Rubric',
            fields=[
                ('codeRubric', models.BigIntegerField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=60, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('username', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('idPerson', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=60)),
                ('carrer', models.CharField(choices=[('2542', 'Ingeniería Civil'), ('2549', 'Ingeniería Química'), ('2547', 'Ingeniería Mecánica'), ('2541', 'Ingeniería Agrícola'), ('2544', 'Ingeniería Eléctrica'), ('2546', 'Ingeniería Industrial'), ('2548', 'Ingeniería Mecatrónica'), ('2545', 'Ingeniería Electrónica'), ('2882', 'Maestría en Bioinformática'), ('2217', 'Especialización en Geotecnia'), ('2285', 'Especialización en Transporte'), ('2886', 'Especialización en Estructuras'), ('2708', 'Maestría en Ingeniería Industrial'), ('2700', 'Maestría en Ingeniería - Geotecnia'), ('2706', 'Maestría en Ingeniería - Transporte'), ('2699', 'Maestría en Ingeniería - Estructuras'), ('2879', 'Ingeniería de Sistemas y Computación'), ('2278', 'Especialización en Recursos Hidráulicos'), ('2896', 'Especialización en Gobierno Electrónico'), ('2113', 'Especialización en Ingeniería Eléctrica'), ('2064', 'Especialización en Calidad de la Energía'), ('2887', 'Doctorado en Ingeniería - Ingeniería Civil'), ('2707', 'Maestría en Ingeniería - Telecomunicaciones'), ('2687', 'Especialización en Automatización Industrial'), ('2704', 'Maestría en Ingeniería - Ingeniería Química'), ('2686', 'Doctorado en Ingeniería - Ingeniería Química'), ('2709', 'Maestría en Ingeniería - Ingeniería Mecánica'), ('2710', 'Maestría en Ingeniería - Materiales y Procesos'), ('2701', 'Maestría en Ingeniería - Ingeniería Agrícola'), ('2705', 'Maestría en Ingeniería - Recursos Hidráulicos'), ('2562', 'Maestría en Ingeniería - Ingeniería Ambiental'), ('2685', 'Doctorado en Ingeniería - Ingeniería Eléctrica'), ('2703', 'Maestría en Ingeniería - Ingeniería Eléctrica'), ('2684', 'Doctorado en Ingeniería - Sistemas y Computación'), ('2691', 'Especialización en Iluminación Pública y Privada'), ('2865', 'Maestría en Ingeniería - Ingeniería Electrónica'), ('2698', 'Maestría en Ingeniería - Automatización Industrial'), ('2838', 'Doctorado en Ingeniería - Industria y Organizaciones'), ('2696', 'Especialización en Transito, Diseño y Seguridad Vial'), ('2682', 'Doctorado en Ingeniería - Ciencia y Tecnología de Materiales'), ('2839', 'Doctorado en Ingeniería - Ingeniería Mecánica y Mecatrónica'), ('2702', 'Maestría en Ingeniería - Ingeniería de Sistemas y Computación'), ('2794', 'Maestría en Ingeniería - Ingeniería Eléctrica Convenio Sede Manizales'), ('2856', 'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv UPC'), ('2928', 'Maestría en Ingeniería - Ingeniería de Sistemas y Computación - Conv Unillanos'), ('2979', 'Doctorado en Estudios Ambientales'), ('BAPI', 'Modalidad de Asignaturas de Posgrado Facultad de Ingeniería')], max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('username', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('idPerson', models.CharField(max_length=60)),
                ('email', models.CharField(max_length=60)),
                ('name', models.CharField(max_length=60)),
                ('departmentDoc', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='StudentOutcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('codeRubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.rubric')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCoEvaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeRubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.rubric')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.course')),
                ('numberGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.groupco')),
                ('studentCOEV1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.student')),
                ('studentCOEV2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.coevaluation')),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceIndicator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('codeSO', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.studentoutcome')),
            ],
        ),
        migrations.CreateModel(
            name='MonitoringPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.CharField(max_length=60)),
                ('actions', models.CharField(max_length=60)),
                ('metodology', models.CharField(max_length=60)),
                ('courses', models.CharField(max_length=60)),
                ('progress', models.CharField(max_length=60)),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.studentoutcome')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementEduResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('measureERPeriod', models.CharField(max_length=60)),
                ('experts', models.IntegerField()),
                ('competents', models.IntegerField()),
                ('apprentices', models.IntegerField()),
                ('beginners', models.IntegerField()),
                ('codeResult', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.studentoutcome')),
                ('codeRubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.rubric')),
            ],
        ),
        migrations.CreateModel(
            name='IndicatorAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codeIA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.performanceindicator')),
                ('idHomework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.homeworkgroupstudent')),
            ],
        ),
        migrations.CreateModel(
            name='ImprovementPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planPeriod', models.CharField(max_length=60)),
                ('diagnosis', models.CharField(max_length=60)),
                ('analysis', models.CharField(max_length=60)),
                ('codeResult', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.studentoutcome')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.teacher')),
            ],
        ),
        migrations.CreateModel(
            name='GroupTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numGroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.groupco')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='groupstudent',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.student'),
        ),
        migrations.AddField(
            model_name='coevaluation',
            name='codeRubric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.rubric'),
        ),
        migrations.AddField(
            model_name='coevaluation',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.course'),
        ),
        migrations.AddField(
            model_name='coevaluation',
            name='numberGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.groupco'),
        ),
        migrations.AddField(
            model_name='coevaluation',
            name='studentCOEV2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.student'),
        ),
        migrations.CreateModel(
            name='AutoEvaluationCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autoPeriod', models.CharField(max_length=60)),
                ('numberStudents', models.IntegerField()),
                ('codeCourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.course')),
                ('codeRubric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.rubric')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='assignment',
            name='codeResult',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.studentoutcome'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='numGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.groupco'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aesci_api.teacher'),
        ),
    ]
