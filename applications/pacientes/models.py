from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    dni = models.CharField(max_length=13, unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')])
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.dni})"
