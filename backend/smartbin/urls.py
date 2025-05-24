from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ZoneViewSet, SmartBinViewSet, CollectionViewSet,
    AlertViewSet, CollectionRouteViewSet, BinReportViewSet,
    TriCenterViewSet, WasteFlowViewSet, CenterStatisticsViewSet,
    tri_center_data_entry
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'zones', ZoneViewSet)
router.register(r'bins', SmartBinViewSet)
router.register(r'collections', CollectionViewSet)
router.register(r'alerts', AlertViewSet)
router.register(r'routes', CollectionRouteViewSet)
router.register(r'reports', BinReportViewSet)
router.register(r'tri-centers', TriCenterViewSet)
router.register(r'waste-flows', WasteFlowViewSet)
router.register(r'center-statistics', CenterStatisticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tri-center/data-entry/', tri_center_data_entry, name='tri_center_data_entry'),
] 