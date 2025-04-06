from django.db import models
from django.contrib.auth.models import User

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


# Create your models here.

class LifestyleTest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('non_binary', 'Non-Binary'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ])
    height = models.CharField(max_length=10)  # Storing as text (e.g., 5'8'')
    weight = models.FloatField()  # Storing weight in kg
    location = models.CharField(max_length=20, choices=[
        ('north_india', 'North India'),
        ('south_india', 'South India'),
        ('east_india', 'East India'),
        ('west_india', 'West India'),
        ('other', 'Other')
    ])
    health_conditions = models.CharField(max_length=20, choices=[
        ('normal', 'Normal'),
        ('hypertension', 'Hypertension'),
        ('diabetes', 'Diabetes'),
        ('asthma', 'Asthma'),
        ('other', 'Other')
    ])
    alcohol_consumption = models.CharField(max_length=20, choices=[
        ('occasionally', 'Occasionally'),
        ('regularly', 'Regularly'),
        ('never', 'Never')
    ])
    sleeping_hours = models.CharField(max_length=20, choices=[
        ('less_than_5', 'Less than 5 hours'),
        ('5_to_7', '5 to 7 hours'),
        ('more_than_7', 'More than 7 hours')
    ])
    lifestyle = models.CharField(max_length=20, choices=[
        ('lying_around', 'Lying Around'),
        ('active', 'Active Lifestyle'),
        ('balanced', 'Balanced Lifestyle'),
        ('social', 'Very Social'),
        ('busy', 'Busy Lifestyle')
    ])
    exercise_regularity = models.CharField(max_length=20, choices=[
        ('everyday', 'Everyday'),
        ('occasionally', 'Occasionally'),
        ('never', 'Never')
    ])
    proud_of = models.CharField(max_length=20, choices=[
        ('strongly_disagree', 'Strongly Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('strongly_agree', 'Strongly Agree')
    ])
    positive_attitude = models.CharField(max_length=20, choices=[
        ('strongly_disagree', 'Strongly Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('strongly_agree', 'Strongly Agree')
    ])
    self_satisfaction = models.CharField(max_length=20, choices=[
        ('strongly_disagree', 'Strongly Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('strongly_agree', 'Strongly Agree')
    ])
    self_respect = models.CharField(max_length=20, choices=[
        ('strongly_disagree', 'Strongly Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('strongly_agree', 'Strongly Agree')
    ])
    feeling_useless = models.CharField(max_length=20, choices=[
        ('strongly_disagree', 'Strongly Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('strongly_agree', 'Strongly Agree')
    ])
    not_good_enough = models.CharField(max_length=20, choices=[
        ('strongly_disagree', 'Strongly Disagree'),
        ('disagree', 'Disagree'),
        ('neutral', 'Neutral'),
        ('agree', 'Agree'),
        ('strongly_agree', 'Strongly Agree')
    ])

    bmi = models.FloatField(null = True, blank = True)
    obesity_level = models.CharField(max_length = 50, null = True, blank=True)

    def calculate_bmi(self):
        """ Convert height to meters and calculate BMI """
        try:
            height_ft, height_in = map(int, self.height.replace('"', '').split("'"))
            height_m = ((height_ft * 12) + height_in) * 0.0254  # Convert to meters
            bmi = self.weight / (height_m ** 2)
            return round(bmi, 2)
        except ValueError:
            return None  # Handle invalid height format

    def obesity_status(self):
        """ Determine obesity level based on BMI """
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal Weight"
        elif 25 <= bmi < 29.9:
            return "Overweight Level I"
        elif 30 <= bmi < 34.9:
            return "Overweight Level II"
        elif 35 <= bmi < 39.9:
            return "Obesity Type I"
        elif 40 <= bmi < 49.9:
            return "Obesity Type II"
        else:
            return"Obesity Type III"

    def __str__(self):
        return f"{self.name} - {self.obesity_status()}"



class LipidTestResult(models.Model):
    haemoglobin_test = models.FloatField()
    waistcircum_test = models.FloatField()
    glucose_test = models.FloatField()
    cholestrol_test = models.FloatField()
    triglycerides_test = models.FloatField()
    ldlipoprotein_test = models.FloatField()
    hdlipoprotein_test = models.FloatField()
    vldlipoprotein_test = models.FloatField()
    hdlratio_test = models.FloatField()
    predicted_risk = models.CharField(max_length=20)  # Store risk level (e.g., "High", "Medium", "Low")
    timestamp = models.DateTimeField(auto_now_add=True)  # Stores the date & time of the test

    def __str__(self):
        return f"Lipid Test - {self.predicted_risk} ({self.timestamp})"



class Symptom(models.Model):
    """
    Model to store individual symptoms.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Disease(models.Model):
    """
    Model to store diseases and their associated symptoms.
    """
    name = models.CharField(max_length=255, unique=True)
    symptoms = models.ManyToManyField(Symptom, related_name="diseases")

    def __str__(self):
        return self.name
    

class UploadedDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #  Keep user
    file = models.FileField(upload_to="uploaded_documents/")  #  Rename document -> file
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  #  Keep only one timestamp

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"
