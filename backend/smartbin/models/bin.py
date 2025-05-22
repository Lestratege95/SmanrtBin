from django.db import models
from django.contrib.auth.models import User

class Bin(models.Model):
    STATUS_CHOICES = [
        ('empty', 'Vide'),
        ('half', 'À moitié plein'),
        ('full', 'Plein'),
        ('overflow', 'Débordement'),
    ]

    TYPE_CHOICES = [
        ('general', 'Général'),
        ('recyclable', 'Recyclable'),
        ('organic', 'Organique'),
        ('hazardous', 'Dangereux'),
    ]

    name = models.CharField(max_length=100, verbose_name="Nom")
    location = models.CharField(max_length=200, verbose_name="Emplacement")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='empty', verbose_name="Statut")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general', verbose_name="Type")
    capacity = models.FloatField(verbose_name="Capacité (L)")
    current_level = models.FloatField(default=0, verbose_name="Niveau actuel (L)")
    last_collection = models.DateTimeField(null=True, blank=True, verbose_name="Dernière collecte")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Assigné à")

    class Meta:
        verbose_name = "Poubelle"
        verbose_name_plural = "Poubelles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_type_display()} ({self.location})"

    def get_fill_percentage(self):
        if self.capacity == 0:
            return 0
        return (self.current_level / self.capacity) * 100 