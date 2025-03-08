# Generated by Django 5.1.6 on 2025-03-03 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0005_symptomstest_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LipidTestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('haemoglobin_test', models.FloatField()),
                ('waistcircum_test', models.FloatField()),
                ('glucose_test', models.FloatField()),
                ('cholestrol_test', models.FloatField()),
                ('triglycerides_test', models.FloatField()),
                ('ldlipoprotein_test', models.FloatField()),
                ('hdlipoprotein_test', models.FloatField()),
                ('vldlipoprotein_test', models.FloatField()),
                ('hdlratio_test', models.FloatField()),
                ('predicted_risk', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='LipidProfileTest',
        ),
    ]
