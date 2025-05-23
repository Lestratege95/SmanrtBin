from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
import uuid

class ModulePermission(models.Model):
    module = models.CharField(max_length=50)
    permission = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('module', 'permission')

    def __str__(self):
        return f"{self.module} - {self.permission}"

class UserRole(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('collector', 'Collecteur'),
        ('tri_agent', 'Agent de tri'),
        ('supervisor', 'Superviseur'),
        ('partner', 'Partenaire'),
    )
    
    name = models.CharField(max_length=50, choices=ROLE_CHOICES)
    description = models.TextField()
    permissions = models.ManyToManyField(ModulePermission)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    ROLES = (
        ('admin', 'Administrateur'),
        ('collector', 'Collecteur'),
        ('citizen', 'Citoyen'),
        ('tri_center', 'Centre de tri'),
        ('tri_agent', 'Agent de tri'),
        ('supervisor', 'Superviseur'),
        ('partner', 'Partenaire'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='citizen')
    phone = models.CharField(max_length=20, blank=True, null=True)
    user_role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Nom unique pour éviter le conflit
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Nom unique pour éviter le conflit
        blank=True,
    )

    
    def has_module_permission(self, module, permission):
        if self.is_superuser:
            return True
        if not self.user_role:
            return False
        return self.user_role.permissions.filter(
            module=module,
            permission=permission
        ).exists()
    
    class Meta:
        app_label = 'smartbin'

class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profil')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    date_naissance = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"


class Zone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class SmartBin(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('maintenance', 'En maintenance'),
        ('inactive', 'Inactive'),
    )
    
    id = models.CharField(max_length=50, primary_key=True)
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True)
    fill_level = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_collection = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bac #{self.id} - {self.location}"

class Collection(models.Model):
    bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE)
    collector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Collecte du {self.date} - Bac #{self.bin.id}"

class Alert(models.Model):
    SEVERITY_CHOICES = (
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    )
    
    bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE)
    type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Alerte {self.type} - Bac #{self.bin.id}"

class CollectionRoute(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
    )
    
    name = models.CharField(max_length=100)
    collector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bins = models.ManyToManyField(SmartBin)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tournée {self.name} - {self.scheduled_date}"

class BinReport(models.Model):
    ISSUE_TYPES = (
        ('broken', 'Cassé'),
        ('full', 'Plein'),
        ('empty', 'Vide'),
        ('other', 'Autre'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('completed', 'Terminée'),
        ('failed', 'Échoué'),
    )
    
    
    bin = models.ForeignKey(SmartBin, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    issue_type = models.CharField(
        max_length=20,
        choices=ISSUE_TYPES,
        default='FULL'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    @property
    def date(self):
        return self.created_at.date()

    def __str__(self):
        return f"Report #{self.id} - {self.get_issue_type_display()}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Signalement de poubelle'
        verbose_name_plural = 'Signalements de poubelles'

class TriCenter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.TextField()
    gps_lat = models.FloatField()
    gps_lng = models.FloatField()
    email_contact = models.EmailField()
    phone = models.CharField(max_length=20)
    total_capacity = models.IntegerField(help_text="Capacité en kg")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class WasteFlow(models.Model):
    WASTE_TYPES = (
        ('plastic', 'Plastique'),
        ('glass', 'Verre'),
        ('paper', 'Papier'),
        ('metal', 'Métal'),
        ('organic', 'Organique'),
        ('other', 'Autre'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tri_center = models.ForeignKey(TriCenter, on_delete=models.CASCADE)
    smart_bin = models.ForeignKey(SmartBin, on_delete=models.SET_NULL, null=True, blank=True)
    processing_date = models.DateTimeField(default=timezone.now)
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPES)
    quantity_kg = models.FloatField()
    recycling_rate = models.FloatField(help_text="Taux de valorisation en %")
    anomaly_detected = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Flux {self.waste_type} - {self.processing_date}"

class CenterStatistics(models.Model):
    PERIOD_CHOICES = (
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    )

    tri_center = models.ForeignKey(TriCenter, on_delete=models.CASCADE)
    period = models.DateField()
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    total_received = models.FloatField(help_text="Total reçu en kg")
    total_recycled = models.FloatField(help_text="Total recyclé en kg")
    collection_count = models.IntegerField()

    class Meta:
        unique_together = ('tri_center', 'period', 'period_type')

    def __str__(self):
        return f"Stats {self.tri_center} - {self.period}"

class Valorization(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('cancelled', 'Annulée'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    waste_flow = models.ForeignKey(WasteFlow, on_delete=models.CASCADE)
    partner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    quantity_kg = models.FloatField()
    price_per_kg = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Valorisation {self.waste_flow.waste_type} - {self.quantity_kg}kg"

class ImpactReport(models.Model):
    PERIOD_CHOICES = (
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    )

    period = models.DateField()
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    total_recycled = models.FloatField(help_text="Total recyclé en kg")
    co2_saved = models.FloatField(help_text="CO2 économisé en kg")
    active_bins = models.IntegerField()
    collection_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Impact {self.period_type} - {self.period}"

class PaymentPlan(models.Model):
    PLAN_TYPES = (
        ('monthly', 'Mensuel'),
        ('quarterly', 'Trimestriel'),
        ('yearly', 'Annuel'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    features = models.JSONField()  # Liste des fonctionnalités incluses
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_plan_type_display()}"

class PaymentMethod(models.Model):
    PAYMENT_TYPES = (
        ('tmoney', 'TMoney'),
        ('flooz', 'Flooz'),
        ('card', 'Carte Bancaire'),
        ('bank_transfer', 'Virement Bancaire'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    account_number = models.CharField(max_length=100)  # Numéro de compte ou carte
    is_default = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'payment_type', 'account_number')

    def __str__(self):
        return f"{self.user.username} - {self.get_payment_type_display()}"

class Subscription(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('pending', 'En attente'),
        ('cancelled', 'Annulée'),
        ('expired', 'Expirée'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_plan = models.ForeignKey(PaymentPlan, on_delete=models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.payment_plan.name}"

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    )
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Paiement #{self.transaction_id} - {self.amount}"

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    )
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pdf_file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Facture #{self.invoice_number}" 