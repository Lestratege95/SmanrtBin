from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Zone, SmartBin, Collection, Alert,
    CollectionRoute, BinReport, UserProfile,
    TriCenter, WasteFlow, CenterStatistics
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'role', 'phone_number', 'zone']
        read_only_fields = ['id']

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ['id', 'name', 'description', 'location', 'manager']
        read_only_fields = ['id']

class SmartBinSerializer(serializers.ModelSerializer):
    zone_name = serializers.CharField(source='zone.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = SmartBin
        fields = [
            'id', 'identifier', 'zone', 'zone_name', 'location',
            'status', 'status_display', 'fill_level', 'last_collection',
            'last_maintenance', 'battery_level'
        ]
        read_only_fields = ['id', 'last_collection', 'last_maintenance']

class CollectionSerializer(serializers.ModelSerializer):
    bin_identifier = serializers.CharField(source='bin.identifier', read_only=True)
    collector_name = serializers.CharField(source='collector.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Collection
        fields = [
            'id', 'bin', 'bin_identifier', 'collector', 'collector_name',
            'status', 'status_display', 'date', 'weight', 'notes'
        ]
        read_only_fields = ['id']

class AlertSerializer(serializers.ModelSerializer):
    bin_identifier = serializers.CharField(source='bin.identifier', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Alert
        fields = [
            'id', 'bin', 'bin_identifier', 'type', 'type_display',
            'status', 'status_display', 'message', 'date', 'resolved_date'
        ]
        read_only_fields = ['id', 'date', 'resolved_date']

class CollectionRouteSerializer(serializers.ModelSerializer):
    collector_name = serializers.CharField(source='collector.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    bins_count = serializers.SerializerMethodField()

    class Meta:
        model = CollectionRoute
        fields = [
            'id', 'collector', 'collector_name', 'status', 'status_display',
            'date', 'bins', 'bins_count', 'notes'
        ]
        read_only_fields = ['id']

    def get_bins_count(self, obj):
        return obj.bins.count()

class BinReportSerializer(serializers.ModelSerializer):
    bin_identifier = serializers.CharField(source='bin.identifier', read_only=True)
    reporter_name = serializers.CharField(source='reporter.get_full_name', read_only=True)
    issue_type_display = serializers.CharField(source='get_issue_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = BinReport
        fields = [
            'id', 'bin', 'bin_identifier', 'reporter', 'reporter_name',
            'issue_type', 'issue_type_display', 'status', 'status_display',
            'description', 'date', 'resolved_date'
        ]
        read_only_fields = ['id', 'date', 'resolved_date']

class TriCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriCenter
        fields = [
            'id', 'name', 'address', 'gps_lat', 'gps_lng',
            'email_contact', 'phone', 'total_capacity', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class WasteFlowSerializer(serializers.ModelSerializer):
    tri_center_name = serializers.CharField(source='tri_center.name', read_only=True)
    bin_identifier = serializers.CharField(source='smart_bin.identifier', read_only=True)
    waste_type_display = serializers.CharField(source='get_waste_type_display', read_only=True)

    class Meta:
        model = WasteFlow
        fields = [
            'id', 'tri_center', 'tri_center_name', 'smart_bin', 'bin_identifier',
            'processing_date', 'waste_type', 'waste_type_display', 'quantity_kg',
            'recycling_rate', 'anomaly_detected', 'comment'
        ]
        read_only_fields = ['id']

class CenterStatisticsSerializer(serializers.ModelSerializer):
    tri_center_name = serializers.CharField(source='tri_center.name', read_only=True)
    period_type_display = serializers.CharField(source='get_period_type_display', read_only=True)

    class Meta:
        model = CenterStatistics
        fields = [
            'id', 'tri_center', 'tri_center_name', 'period', 'period_type',
            'period_type_display', 'total_received', 'total_recycled',
            'collection_count'
        ]
        read_only_fields = ['id']

class StatisticsSerializer(serializers.Serializer):
    total_bins = serializers.IntegerField()
    full_bins = serializers.IntegerField()
    average_fill_level = serializers.FloatField()
    today_collections = serializers.IntegerField()
    collections_by_day = serializers.ListField(
        child=serializers.DictField()
    ) 