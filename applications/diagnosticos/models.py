from django.db import models
# Ya no necesitas importar directamente Patient

class Diagnosis(models.Model):
    patient = models.ForeignKey('pacientes.Patient', on_delete=models.CASCADE, verbose_name='Paciente', related_name='diagnoses')
    date = models.DateTimeField(verbose_name='Fecha y Hora', auto_now_add=True)
    description = models.TextField(verbose_name='Descripción')
    icd_code = models.CharField(verbose_name='Código CIE', max_length=10, null=True, blank=True)
    notes = models.TextField(verbose_name='Notas Adicionales', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Activo', default=True)

    def __str__(self):
        return f"Diagnóstico de {self.patient} - {self.date.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['-date']
