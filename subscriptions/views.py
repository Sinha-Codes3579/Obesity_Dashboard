from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .models import Subscriber
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.clickjacking import xframe_options_exempt
from .models import LifestyleTest, LipidTestResult, Disease, Symptom, UploadedDocument
from django.core.files.storage import FileSystemStorage
from .forms import LipidTestForm, DocumentUploadForm
from django.db.models.signals import post_migrate
from django.dispatch import receiver
import json
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd
import re
import matplotlib
import numpy as np
import joblib
matplotlib.use('Agg')

# for subscription of website
@csrf_protect  # Optional: If CSRF token issues occur (not recommended for production)
def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({"error": "This email is already subscribed!"}, status=400)
        
        Subscriber.objects.create(email=email)
        return JsonResponse({"message": "Subscription successful!"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


def home(request):
    try:
        return render(request, "index.html")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
# login into main page
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        password2 = request.POST.get("password2", "").strip()

        if not username or not email or not password or not password2:
            messages.error(request, "All fields are required.")
            return redirect("signup")

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("login")

    return render(request, "signup.html")


# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")
@login_required
def dashboard(request):
    return render(request,"dashboard.html")

@login_required
def lifestyle_test(request):
    return render(request, "lifestyle_test.html")

@login_required
def lipid_test(request):
    return render(request, "lipid_test.html")

@login_required
def symptoms_test(request):
    return render(request, "symptoms_test.html")

@xframe_options_exempt
def flower_page(request):
    return render(request, "flower.html")



def load_dataset():
    global df  # Make df accessible if needed elsewhere
    file = r"C:\Users\sinha\Obesity_Dashboard\ObesityDataSet.csv"
    df = pd.read_csv(file)
    print(df.columns)  # Debugging (remove if not needed)
    df["Height"] = df["Height"] / 100  # Convert once
    df["BMI"] = df["Weight"] / (df["Height"] ** 2)
# classification of obesity level based on bmi
def classify_obesity(bmi):
    load_dataset()
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
@csrf_protect
def lifestyle_test_api(request):
    load_dataset()
    if(request.method == "POST"):
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            age = int(request.POST.get('age'))
            gender = request.POST.get('gender')
            height = request.POST.get('height')  # Expected format: "5'8''"
            weight = float(request.POST.get('weight'))

            # Validate and parse height correctly
            try:
                feet, inches = map(int, re.findall(r"\d+", height))
                height_meters = (feet * 0.3048) + (inches * 0.0254)
            except ValueError:
                return JsonResponse({"error": "Invalid height format. Use format like 5'8''"}, status=400)

            bmi = weight / (height_meters ** 2)
            obesity_level = classify_obesity(bmi)

            # Ensure all required fields exist
            required_fields = [
                "name", "email", "age", "gender", "height", "weight", "location",
                "health_conditions", "alcohol_consumption", "sleeping_hours",
                "lifestyle", "exercise_regularity", "proud_of", "positive_attitude",
                "self_satisfaction", "self_respect", "feeling_useless", "not_good_enough"
            ]
            missing_fields = [field for field in required_fields if not request.POST.get(field)]
            if missing_fields:
                return JsonResponse({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=400)

            # Save to DB
            LifestyleTest.objects.create(
                name=name, email=email, age=age, gender=gender, weight=weight, height=height,
                location=request.POST.get('location'),
                health_conditions=request.POST.get('health_conditions'),
                alcohol_consumption=request.POST.get('alcohol_consumption'),
                sleeping_hours=request.POST.get('sleeping_hours'),
                lifestyle=request.POST.get('lifestyle'),
                exercise_regularity=request.POST.get('exercise_regularity'),
                proud_of=request.POST.get('proud_of'),
                positive_attitude=request.POST.get('positive_attitude'),
                self_satisfaction=request.POST.get('self_satisfaction'),
                self_respect=request.POST.get('self_respect'),
                feeling_useless=request.POST.get('feeling_useless'),
                not_good_enough=request.POST.get('not_good_enough'),
                bmi=bmi,
                obesity_level=obesity_level,
            )

            # Generate relevant graphs
            obesity_graph = generate_obesity_graph(df)
            lifestyle_graph = generate_lifestyle_graph(df)
            mental_health_graph = generate_mental_health_graph(df)
            
            return JsonResponse({
                "message": "Form submitted successfully!",
                "bmi": round(bmi, 2),
                "obesity_level": obesity_level,
                "obesity_graph": obesity_graph if obesity_graph else None,
                "lifestyle_graph": lifestyle_graph if lifestyle_graph else None,
                "mental_health_graph": mental_health_graph if mental_health_graph else None,
            })
           
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
    
    return JsonResponse({"error" : "Invalid Request!"}, status = 400)
# function to generate obesity level distribution graph
def generate_obesity_graph(df):
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="NObeyesdad", hue="NObeyesdad", palette="coolwarm", legend=False)
    plt.title("Obesity Level Distribution", fontsize = 14)
    plt.xlabel("Obesity Level")
    plt.ylabel("count")
    img = io.BytesIO()
    plt.savefig(img, format = "png")
    img.seek(0)
    return f"data:image/png; base64, {base64.b64encode(img.read()).decode('utf-8')}"
# Function to analyze lifestyle choices (e.g., exercise vs. obesity)
def generate_lifestyle_graph(df):
    if "BMI" not in df.columns:
        return None
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x="FAF", y="BMI", hue="FAF", palette="viridis", legend=False)
    plt.title("Exercise Frequency vs. Obesity", fontsize=14)
    plt.xlabel("Exercise Frequency (FAF)")
    plt.ylabel("BMI")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return f"data:image/png;base64,{base64.b64encode(img.read()).decode('utf-8')}"
# Function to analyze mental health indicators
def generate_mental_health_graph(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df["CALC"], bins=3, kde=True, color="purple")
    plt.title("Alcohol Consumption vs. Mental Health", fontsize=14)
    plt.xlabel("Alcohol Consumption (CALC)")
    plt.ylabel("Frequency")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return f"data:image/png;base64,{base64.b64encode(img.read()).decode('utf-8')}"


model = joblib.load("subscriptions/models/adaboost_model.pkl")
scaler = joblib.load("subscriptions/models/scaler.pkl")
@csrf_protect
def lipid_test_view(request):
    risk_result = None  # Store risk level
    form = LipidTestForm()

    if request.method == "POST":
        form = LipidTestForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Extract user inputs
            user_features = np.array([
                data["haemoglobin_test"],
                data["waistcircum_test"],
                data["glucose_test"],
                data["ldlipoprotein_test"],
                data["hdlipoprotein_test"],
                data["hdlratio_test"]
            ])

            # Model features from the form
            model_features = np.array([
                data["cholestrol_test"],
                data["triglycerides_test"],
                data["vldlipoprotein_test"]
            ])

            # Combine inputs
            input_data = np.concatenate((user_features, model_features)).reshape(1, -1)

            # Scale input data
            input_data_scaled = scaler.transform(input_data)

            # Predict using AdaBoost model
            prediction = model.predict(input_data_scaled)[0]

            # Define threshold-based risk conditions
            risk_result = determine_risk_level(data, prediction)
            
        
            # save the result in database

            LipidTestResult.objects.create(
                haemoglobin_test=data["haemoglobin_test"],
                waistcircum_test=data["waistcircum_test"],
                glucose_test=data["glucose_test"],
                cholestrol_test=data["cholestrol_test"],
                triglycerides_test=data["triglycerides_test"],
                ldlipoprotein_test=data["ldlipoprotein_test"],
                hdlipoprotein_test=data["hdlipoprotein_test"],
                vldlipoprotein_test=data["vldlipoprotein_test"],
                hdlratio_test=data["hdlratio_test"],
                predicted_risk=risk_result
            )
            return JsonResponse({"risk_level": risk_result})

    return render(request, "lipid_test.html", {"form": form, "risk_result": risk_result})


def determine_risk_level(data, model_prediction):
    """Determine risk based on thresholds and model prediction."""
    
    high_risk = (
        data["cholestrol_test"] >= 240 or
        data["triglycerides_test"] >= 200 or
        data["ldlipoprotein_test"] >= 160 or
        data["hdlipoprotein_test"] < 40 or
        data["haemoglobin_test"] < 12 or
        data["waistcircum_test"] > 102 or
        data["glucose_test"] >= 126 or
        data["hdlratio_test"] > 4.5
    )

    moderate_risk = (
        200 <= data["cholestrol_test"] < 240 or
        150 <= data["triglycerides_test"] < 200 or
        130 <= data["ldlipoprotein_test"] < 160 or
        40 <= data["hdlipoprotein_test"] < 50 or
        12 <= data["haemoglobin_test"] < 14 or
        94 <= data["waistcircum_test"] <= 102 or
        100 <= data["glucose_test"] < 126 or
        3.5 <= data["hdlratio_test"] <= 4.5
    )

    # Machine learning prediction (if you want to use it)
    risk_mapping = {0: "Low Risk", 1: "Moderate Risk", 2: "High Risk"}
    ml_result = risk_mapping[model_prediction]

    # Final Decision (Combine Model & Threshold Logic)
    if high_risk:
        return "High Risk"
    elif moderate_risk:
        return "Moderate Risk"
    else:
        return ml_result  # Use ML prediction if no high/moderate risks

def populate_diseases():
    diseases = [
        {"name": "Diabetes", "symptoms": ["polyuria", "excessive_hunger", "increased_appetite", "fatigue_after_minimal_activity", "dark_patches_on_skin", "slow_healing_of_wounds"]},
        {"name": "Heart Attack", "symptoms": ["chest_pain", "shortness_of_breath", "high_blood_pressure", "excessive_sweating"]},
        {"name": "Hypertension", "symptoms": ["high_blood_pressure", "chest_pain", "shortness_of_breath", "fatigue_after_minimal_activity"]},
        {"name": "Osteoarthritis", "symptoms": ["knee_pain", "joint_pain", "stiffness_in_joints", "painful_walking"]},
        {"name": "Varicose Veins", "symptoms": ["swollen_blood_vessels", "swollen_legs", "prominent_veins_on_calf", "varicose_veins", "painful_walking"]},
        {"name": "Sleep Apnea", "symptoms": ["snoring", "difficulty_breathing_while_lying_down", "chronic_fatigue", "frequent_waking_during_sleep"]},
        {"name": "Depression", "symptoms": ["depression_or_low_mood", "anxiety", "poor_self-esteem", "social_withdrawal"]},
        {"name": "Unknown Condition", "symptoms": ["loss_of_balance", "lack_of_concentration"]}
    ]
    for disease_data in diseases:
        disease, created = Disease.objects.get_or_create(name=disease_data["name"])
        for symptom_name in disease_data["symptoms"]:
            symptom, _ = Symptom.objects.get_or_create(name=symptom_name.replace("_", " "))
            disease.symptoms.add(symptom)


    print("🎉 Database successfully populated!")
@receiver(post_migrate)
def populate_data(sender, **kwargs):
    if sender.name == "subscriptions":  # Replace with your actual app name
        populate_diseases()
@csrf_protect
def symptoms_test_api(request):
    if(request.method == "POST"):
        try:
            raw_body = request.body.decode("utf-8")
            print("🛠 Raw Request Body:", raw_body)
            if not raw_body:
                return JsonResponse({"error": "Empty request body"}, status=400)
            data = json.loads(raw_body)
            selected_symptoms = set(symptom.replace("_", " ").lower().strip() for symptom in data.get("selectedSymptoms", []))
            print("Received Symptoms from Frontend:", selected_symptoms)
            diseases = Disease.objects.all()
            if not diseases.exists():
                print("❌ No diseases found in the database!")
                return JsonResponse({"error": "No disease data available"}, status=500)
            disease_scores = []
            matched_diseases = []
            for disease in diseases:
                disease_symptoms = set(symptom.name.lower() for symptom in disease.symptoms.all())
            
                match_count = len(selected_symptoms.intersection(disease_symptoms))
                print(f"Disease: {disease.name}, Symptoms in DB: {disease_symptoms}")
                if match_count > 0:
                    disease_scores.append((disease.name, match_count))
            if not disease_scores:
                return JsonResponse({"bestMatch": "No disease match found", "matchedDiseases": []})
            disease_scores.sort(key=lambda x: x[1], reverse=True)
            best_match = disease_scores[0][0] if disease_scores else "No disease match found"
            matched_diseases = [d[0] for d in disease_scores]
            
             # **Store the result in the session**
            request.session["health_status"] = {
                "bestMatch": best_match,
                "matchedDiseases": matched_diseases,
                "recommendation": "Consult a healthcare provider for further assessment."
            }

            return JsonResponse({"bestMatch": best_match, "matchedDiseases": matched_diseases, "recommendation": "Consult a healthcare provider for further assessment."})
        except json.JSONDecodeError as e:
            print("❌ JSON Parsing Error:", str(e))
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            print("❌ Unexpected Server Error:", str(e))
            return JsonResponse({"error": "Internal Server Error"}, status=500)
    return JsonResponse({"error": "Invalid Request!"}, status=400)


@login_required
def health_status_view(request):
    # Retrieve latest lipid test result
    latest_test = LipidTestResult.objects.order_by('-timestamp').first()

    # Retrieve session-based health status (if exists)
    health_status = request.session.get("health_status", None)

    return render(request, "health_status.html", {
        "latest_test": latest_test,
        "health_status": health_status
    })

@login_required
def upload_document(request):
    if request.method == "POST":
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)  # Don't save yet
            document.user = request.user  # Assign logged-in user
            document.save()
            return redirect("upload_document_success")
    else:
        form = DocumentUploadForm()

    return render(request, "upload_document.html", {"form": form})
