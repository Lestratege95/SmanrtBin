from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from .models import User, Zone, SmartBin, Collection, Alert, CollectionRoute, BinReport, UserProfile, TriCenter, WasteFlow, CenterStatistics
from .serializers import (
    UserSerializer, ZoneSerializer, SmartBinSerializer, CollectionSerializer,
    AlertSerializer, CollectionRouteSerializer, BinReportSerializer,
    UserProfileSerializer, TriCenterSerializer, WasteFlowSerializer,
    CenterStatisticsSerializer
)
from .permissions import (
    IsAdminOrReadOnly, IsCollector, IsZoneManager, IsBinOwner, IsReportOwner,
    IsResident, IsCollectionOwner, IsTriCenterManager, HasModulePermission
)
from django.contrib.auth import get_user_model
from django.db.models import Count, Avg, F, ExpressionWrapper, FloatField
from django.utils import timezone
from datetime import timedelta
from .filters import (
    SmartBinFilter, CollectionFilter, AlertFilter,
    CollectionRouteFilter, BinReportFilter, TriCenterFilter,
    WasteFlowFilter, CenterStatisticsFilter
)
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'manager']

class SmartBinViewSet(viewsets.ModelViewSet):
    queryset = SmartBin.objects.all()
    serializer_class = SmartBinSerializer
    permission_classes = [IsAdminOrReadOnly | IsZoneManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SmartBinFilter

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        bin = self.get_object()
        new_status = request.data.get('status')
        if new_status:
            bin.status = new_status
            bin.save()
            return Response({'status': 'success'})
        return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly | IsCollector | IsCollectionOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionFilter

    def get_queryset(self):
        user = self.request.user
        if user.role == 'collector':
            return Collection.objects.filter(collector=user)
        return Collection.objects.all()

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAdminOrReadOnly | IsZoneManager | IsBinOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AlertFilter

    def get_queryset(self):
        user = self.request.user
        if user.role == 'citizen':
            return Alert.objects.filter(bin__zone=user.zone)
        return Alert.objects.all()

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.status = 'resolved'
        alert.save()
        return Response({'status': 'success'})

class CollectionRouteViewSet(viewsets.ModelViewSet):
    queryset = CollectionRoute.objects.all()
    serializer_class = CollectionRouteSerializer
    permission_classes = [IsAdminOrReadOnly | IsCollector]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionRouteFilter

    def get_queryset(self):
        user = self.request.user
        if user.role == 'collector':
            return CollectionRoute.objects.filter(collector=user)
        return CollectionRoute.objects.all()

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        route = self.get_object()
        route.status = 'completed'
        route.save()
        return Response({'status': 'success'})

class BinReportViewSet(viewsets.ModelViewSet):
    queryset = BinReport.objects.all()
    serializer_class = BinReportSerializer
    permission_classes = [IsAdminOrReadOnly | IsZoneManager | IsReportOwner | IsResident]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BinReportFilter

    def get_queryset(self):
        user = self.request.user
        if user.role == 'citizen':
            return BinReport.objects.filter(bin__zone=user.zone)
        return BinReport.objects.all()

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        report = self.get_object()
        report.status = 'resolved'
        report.save()
        return Response({'status': 'success'})

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'zone']

class StatisticsViewSet(viewsets.ViewSet):
    permission_classes = [HasModulePermission]

    def list(self, request):
        user = request.user
        if user.role == 'admin':
            # Statistiques globales
            total_bins = SmartBin.objects.count()
            total_collections = Collection.objects.count()
            total_alerts = Alert.objects.count()
            avg_fill_level = SmartBin.objects.aggregate(avg=Avg('fill_level'))['avg']
            
            # Statistiques par zone
            zone_stats = Zone.objects.annotate(
                bin_count=Count('smartbin'),
                avg_fill_level=Avg('smartbin__fill_level')
            ).values('name', 'bin_count', 'avg_fill_level')

            return Response({
                'total_bins': total_bins,
                'total_collections': total_collections,
                'total_alerts': total_alerts,
                'avg_fill_level': avg_fill_level,
                'zone_stats': zone_stats
            })
        elif user.role == 'collector':
            # Statistiques du collecteur
            today = timezone.now().date()
            weekly_collections = Collection.objects.filter(
                collector=user,
                collection_date__gte=today - timedelta(days=7)
            ).count()
            
            bins_collected = Collection.objects.filter(
                collector=user,
                collection_date__gte=today - timedelta(days=30)
            ).values('bin').distinct().count()

            return Response({
                'weekly_collections': weekly_collections,
                'bins_collected': bins_collected
            })
        elif user.role == 'citizen':
            # Statistiques de la zone du citoyen
            zone_bins = SmartBin.objects.filter(zone=user.zone)
            avg_fill_level = zone_bins.aggregate(avg=Avg('fill_level'))['avg']
            alerts_count = Alert.objects.filter(bin__zone=user.zone).count()

            return Response({
                'avg_fill_level': avg_fill_level,
                'alerts_count': alerts_count
            })

def tri_center_data_entry(request):
    if not request.user.is_authenticated:
        return redirect('http://localhost:3000/login')
    
    if not (request.user.is_staff or request.user.role == 'tri_center'):
        return HttpResponseForbidden("Vous n'avez pas les permissions nécessaires")
    
    tri_centers = TriCenter.objects.all()
    smart_bins = SmartBin.objects.all()
    
    return render(request, 'tri_center_data_entry.html', {
        'tri_centers': tri_centers,
        'smart_bins': smart_bins
    })

class TriCenterViewSet(viewsets.ModelViewSet):
    queryset = TriCenter.objects.all()
    serializer_class = TriCenterSerializer
    permission_classes = [IsAdminOrReadOnly | IsTriCenterManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TriCenterFilter

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        center = self.get_object()
        stats = CenterStatistics.objects.filter(tri_center=center)
        serializer = CenterStatisticsSerializer(stats, many=True)
        return Response(serializer.data)

class WasteFlowViewSet(viewsets.ModelViewSet):
    queryset = WasteFlow.objects.all()
    serializer_class = WasteFlowSerializer
    permission_classes = [IsAdminOrReadOnly | IsTriCenterManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WasteFlowFilter

    @action(detail=False, methods=['get'])
    def by_waste_type(self, request):
        waste_type = request.query_params.get('waste_type')
        if waste_type:
            flows = self.get_queryset().filter(waste_type=waste_type)
            serializer = self.get_serializer(flows, many=True)
            return Response(serializer.data)
        return Response({'error': 'waste_type parameter is required'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class CenterStatisticsViewSet(viewsets.ModelViewSet):
    queryset = CenterStatistics.objects.all()
    serializer_class = CenterStatisticsSerializer
    permission_classes = [IsAdminOrReadOnly | IsTriCenterManager]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CenterStatisticsFilter

    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        stats = self.get_queryset().filter(period_type='monthly')
        serializer = self.get_serializer(stats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def yearly_summary(self, request):
        stats = self.get_queryset().filter(period_type='yearly')
        serializer = self.get_serializer(stats, many=True)
        return Response(serializer.data) 