from django import forms
from .models import Subscriber, LipidTestResult, UploadedDocument

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']


class LipidTestForm(forms.ModelForm):
    class Meta:
        model = LipidTestResult
        fields = [
            "haemoglobin_test", "waistcircum_test", "glucose_test", 
            "cholestrol_test", "triglycerides_test", "ldlipoprotein_test", 
            "hdlipoprotein_test", "vldlipoprotein_test", "hdlratio_test"
        ]
    haemoglobin_test = forms.FloatField(label="Haemoglobin Alc (%)", min_value=0, max_value=14)
    waistcircum_test = forms.FloatField(label="Waist Circumference (cm)", min_value=0, max_value=150)
    glucose_test = forms.FloatField(label="Fasting Plasma Glucose (mg/dL)", min_value=0, max_value=300)
    cholestrol_test = forms.FloatField(label="Total Cholesterol (mg/dL)", min_value=0, max_value=400)
    triglycerides_test = forms.FloatField(label="High Triglycerides (mg/dL)", min_value=0, max_value=1000)
    ldlipoprotein_test = forms.FloatField(label="Low-Density Lipoprotein (mg/dL)", min_value=0, max_value=250)
    hdlipoprotein_test = forms.FloatField(label="High-Density Lipoprotein (HDL)", min_value=0, max_value=100)
    vldlipoprotein_test = forms.FloatField(label="Very Low-Density Lipoprotein (VLDL)", min_value=0, max_value=80)
    hdlratio_test = forms.FloatField(label="Cholesterol/HDL Ratio", min_value=0, max_value=8.0)


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedDocument
        fields = ['file', 'description']
        exclude = ['user']  # Exclude user because it's set in the view
