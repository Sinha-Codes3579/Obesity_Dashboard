# Generated by Django 5.1.6 on 2025-02-24 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0002_subscriber_delete_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='LifestyleTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('height', models.CharField(max_length=10)),
                ('weight', models.FloatField()),
                ('location', models.CharField(max_length=50)),
                ('health_conditions', models.CharField(max_length=50)),
                ('alcohol_consumption', models.CharField(max_length=20)),
                ('sleeping_hours', models.CharField(max_length=20)),
                ('lifestyle', models.CharField(max_length=50)),
                ('exercise_regularity', models.CharField(max_length=20)),
                ('proud_of', models.CharField(max_length=50)),
                ('positive_attitude', models.CharField(max_length=50)),
                ('self_satisfaction', models.CharField(max_length=50)),
                ('self_respect', models.CharField(max_length=50)),
                ('feeling_useless', models.CharField(max_length=50)),
                ('not_good_enough', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LipidProfileTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('haemoglobin_test', models.FloatField(help_text='Haemoglobin Alc (HbAlc) Test for Diabetes (%)')),
                ('waistcircum_test', models.FloatField(help_text='Waist Circumference (cm)')),
                ('glucose_test', models.FloatField(help_text='Fasting Plasma Glucose (mg/dL)')),
                ('cholestrol_test', models.FloatField(help_text='Total Cholesterol (mg/dL)')),
                ('triglycerides_test', models.FloatField(help_text='High Triglycerides (mg/dL)')),
                ('ldlipoprotein_test', models.FloatField(help_text='Low-Density Lipoprotein (LDL) (mg/dL)')),
                ('hdlipoprotein_test', models.FloatField(help_text='High-Density Lipoprotein (HDL) (mg/dL)')),
                ('vldlipoprotein_test', models.FloatField(help_text='Very Low-Density Lipoprotein (VLDL)')),
                ('hdlratio_test', models.FloatField(help_text='Cholesterol/HDL Ratio')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='symptomsTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_symptoms', models.TextField(help_text='Comma-separated list of selected symptoms')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
