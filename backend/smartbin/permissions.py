from rest_framework import permissions
from .models import User

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsCollector(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'collector'

class IsZoneManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'zone_manager'

class IsBinOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.zone == obj.zone

class IsReportOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj.reporter

class IsResident(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'citizen'

class IsCollectionOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj.collector

class IsTriCenterManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role in ['tri_center', 'tri_agent']

class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'supervisor'

class IsPartner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'partner'

class HasModulePermission(permissions.BasePermission):
    def __init__(self, module, permission):
        self.module = module
        self.permission = permission

    def has_permission(self, request, view):
        return request.user and request.user.has_module_permission(self.module, self.permission)

# Permissions spécifiques aux modules
class SmartBinPermissions:
    view = HasModulePermission('smart_bins', 'view_smartbin')
    manage = HasModulePermission('smart_bins', 'manage_smartbin')

class CollectionPermissions:
    view = HasModulePermission('collection', 'view_collection')
    manage = HasModulePermission('collection', 'manage_collection')

class TriCenterPermissions:
    view = HasModulePermission('tri_center', 'view_tricenter')
    manage = HasModulePermission('tri_center', 'manage_tricenter')

class ValorizationPermissions:
    view = HasModulePermission('valorization', 'view_valorization')
    manage = HasModulePermission('valorization', 'manage_valorization')

class UserPermissions:
    view = HasModulePermission('users', 'view_users')
    manage = HasModulePermission('users', 'manage_users')

class ReportingPermissions:
    view = HasModulePermission('reporting', 'view_reports')
    manage = HasModulePermission('reporting', 'manage_reports')

class SettingsPermissions:
    view = HasModulePermission('settings', 'view_settings')
    manage = HasModulePermission('settings', 'manage_settings')

class PaymentPermissions:
    view = HasModulePermission('payment', 'view_payment')
    manage = HasModulePermission('payment', 'manage_payment')

class IsPaymentOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, (Payment, Subscription, PaymentMethod)):
            return request.user and request.user == obj.user
        return False

class CanManagePayment(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and (
            request.user.is_staff or 
            request.user.has_module_permission('payment', 'manage_payment')
        ) 