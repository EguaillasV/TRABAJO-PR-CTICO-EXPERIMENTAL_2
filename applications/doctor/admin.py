from django.contrib import admin
from .models import Diagnosis

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'icd_code', 'is_active')
    search_fields = ('patient__nombres', 'description', 'icd_code')
    list_filter = ('is_active', 'date')