from django.contrib import admin
from .models import Subscriber, UploadedDocument, LifestyleTest

admin.site.register(Subscriber)
admin.site.register(LifestyleTest)
admin.site.register(UploadedDocument)

# Register your models here.
