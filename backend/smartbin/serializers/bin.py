from rest_framework import serializers
from ..models.bin import Bin

class BinSerializer(serializers.ModelSerializer):
    fill_percentage = serializers.SerializerMethodField()
    assigned_to_name = serializers.SerializerMethodField()

    class Meta:
        model = Bin
        fields = [
            'id', 'name', 'location', 'status', 'type',
            'capacity', 'current_level', 'last_collection',
            'created_at', 'updated_at', 'assigned_to',
            'fill_percentage', 'assigned_to_name'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_fill_percentage(self, obj):
        return obj.get_fill_percentage()

    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name() or obj.assigned_to.username
        return None

    def validate_current_level(self, value):
        if value < 0:
            raise serializers.ValidationError("Le niveau ne peut pas être négatif")
        if value > self.instance.capacity if self.instance else 0:
            raise serializers.ValidationError("Le niveau ne peut pas dépasser la capacité")
        return value 