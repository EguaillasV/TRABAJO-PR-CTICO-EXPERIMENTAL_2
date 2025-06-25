from django.contrib import admin
from .models import Diagnosis

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'icd_code', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('patient__nombre', 'description', 'icd_code', 'notes')
    ordering = ('-date',)
