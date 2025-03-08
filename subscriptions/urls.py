from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.shortcuts import render
from .views import (
    subscribe, login_view, dashboard, signup_view, logout_view,
    lifestyle_test, lipid_test, symptoms_test, flower_page, lifestyle_test_api, symptoms_test_api,lipid_test_view, upload_document, populate_diseases, health_status_view
)

# sunscription
urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('dashboard/', dashboard, name='dashboard'),
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("flower/", flower_page, name="flower_page"),
    path("lifestyle-test/", lifestyle_test, name="lifestyle_test"),
    path("lipid-test/", lipid_test, name="lipid_test"),
    path("symptoms-test/", symptoms_test, name="symptoms_test"),
    path('api/lifestyle-test/', lifestyle_test_api, name='lifestyle_test_api'),
    path('api/symptoms-test/', symptoms_test_api, name='symptoms_test_api'),
    path("api/populate-diseases/", populate_diseases, name="populate_diseases"),
    path('api/lipid_test/', lipid_test_view, name='lipid_test_view'),
    path("upload-document/", upload_document, name="upload_document"),
    path("health_status/", health_status_view, name="health_status"),
]

