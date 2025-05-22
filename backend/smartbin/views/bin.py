from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.bin import Bin
from ..serializers.bin import BinSerializer
from django.utils import timezone

class BinViewSet(viewsets.ModelViewSet):
    queryset = Bin.objects.all()
    serializer_class = BinSerializer

    def get_queryset(self):
        queryset = Bin.objects.all()
        status = self.request.query_params.get('status', None)
        type = self.request.query_params.get('type', None)
        location = self.request.query_params.get('location', None)

        if status:
            queryset = queryset.filter(status=status)
        if type:
            queryset = queryset.filter(type=type)
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    @action(detail=True, methods=['post'])
    def update_level(self, request, pk=None):
        bin = self.get_object()
        new_level = request.data.get('current_level')

        if new_level is None:
            return Response(
                {"error": "Le niveau actuel est requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            new_level = float(new_level)
        except ValueError:
            return Response(
                {"error": "Le niveau doit être un nombre"},
                status=status.HTTP_400_BAD_REQUEST
            )

        bin.current_level = new_level
        
        # Mise à jour du statut en fonction du niveau
        fill_percentage = bin.get_fill_percentage()
        if fill_percentage >= 100:
            bin.status = 'overflow'
        elif fill_percentage >= 75:
            bin.status = 'full'
        elif fill_percentage >= 25:
            bin.status = 'half'
        else:
            bin.status = 'empty'

        bin.save()
        return Response(BinSerializer(bin).data)

    @action(detail=True, methods=['post'])
    def collect(self, request, pk=None):
        bin = self.get_object()
        bin.current_level = 0
        bin.status = 'empty'
        bin.last_collection = timezone.now()
        bin.save()
        return Response(BinSerializer(bin).data) 