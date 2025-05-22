import django_filters
from django_filters import rest_framework as filters
from .models import (
    SmartBin, Collection, Alert, CollectionRoute,
    BinReport, TriCenter, WasteFlow, CenterStatistics,
    PaymentPlan, PaymentMethod, Subscription, Payment, Invoice
)

class SmartBinFilter(django_filters.FilterSet):
    zone = django_filters.NumberFilter(field_name='zone')
    status = django_filters.ChoiceFilter(choices=SmartBin.STATUS_CHOICES)
    fill_level = django_filters.NumberFilter(method='filter_fill_level')

    class Meta:
        model = SmartBin
        fields = ['zone', 'status', 'fill_level']

    def filter_fill_level(self, queryset, name, value):
        return queryset.filter(fill_level__gte=value)

class CollectionFilter(django_filters.FilterSet):
    bin = django_filters.NumberFilter(field_name='bin')
    collector = django_filters.NumberFilter(field_name='collector')
    status = django_filters.ChoiceFilter(choices=CollectionRoute.STATUS_CHOICES)
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Collection
        fields = ['bin', 'collector', 'status', 'date']

class AlertFilter(django_filters.FilterSet):
    bin = django_filters.NumberFilter(field_name='bin')
    type = django_filters.ChoiceFilter(choices=Alert.SEVERITY_CHOICES)
    # status = django_filters.ChoiceFilter(choices=Alert.STATUS_CHOICES)
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Alert
        fields = ['bin', 'type', 'date']

class CollectionRouteFilter(django_filters.FilterSet):
    collector = django_filters.NumberFilter(field_name='collector')
    status = django_filters.ChoiceFilter(choices=CollectionRoute.STATUS_CHOICES)
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = CollectionRoute
        fields = ['collector', 'status', 'date']

class BinReportFilter(django_filters.FilterSet):
    bin = django_filters.NumberFilter(field_name='bin')
    reporter = django_filters.NumberFilter(field_name='reporter')
    issue_type = django_filters.ChoiceFilter(choices=BinReport.ISSUE_TYPES)
    status = django_filters.ChoiceFilter(choices=BinReport.STATUS_CHOICES)
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = BinReport
        fields = ['bin', 'reporter', 'issue_type', 'status', 'date']

class TriCenterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    total_capacity = django_filters.NumberFilter(method='filter_capacity')
    date_created = django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = TriCenter
        fields = ['name', 'total_capacity', 'date_created']

    def filter_capacity(self, queryset, name, value):
        return queryset.filter(total_capacity__gte=value)

class WasteFlowFilter(django_filters.FilterSet):
    tri_center = django_filters.NumberFilter(field_name='tri_center')
    smart_bin = django_filters.NumberFilter(field_name='smart_bin')
    waste_type = django_filters.ChoiceFilter(choices=WasteFlow.WASTE_TYPES)
    processing_date = django_filters.DateFromToRangeFilter()
    recycling_rate = django_filters.NumberFilter(method='filter_recycling_rate')
    anomaly_detected = django_filters.BooleanFilter()

    class Meta:
        model = WasteFlow
        fields = [
            'tri_center', 'smart_bin', 'waste_type',
            'processing_date', 'recycling_rate', 'anomaly_detected'
        ]

    def filter_recycling_rate(self, queryset, name, value):
        return queryset.filter(recycling_rate__gte=value)

class CenterStatisticsFilter(django_filters.FilterSet):
    tri_center = django_filters.NumberFilter(field_name='tri_center')
    period_type = django_filters.ChoiceFilter(choices=CenterStatistics.PERIOD_CHOICES)
    period = django_filters.DateFromToRangeFilter()
    total_received = django_filters.NumberFilter(method='filter_total_received')
    total_recycled = django_filters.NumberFilter(method='filter_total_recycled')

    class Meta:
        model = CenterStatistics
        fields = [
            'tri_center', 'period_type', 'period',
            'total_received', 'total_recycled'
        ]

    def filter_total_received(self, queryset, name, value):
        return queryset.filter(total_received__gte=value)

    def filter_total_recycled(self, queryset, name, value):
        return queryset.filter(total_recycled__gte=value)

class PaymentPlanFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    plan_type = filters.ChoiceFilter(choices=PaymentPlan.PLAN_TYPES)
    # status = filters.ChoiceFilter(choices=PaymentPlan.STATUS_CHOICES)
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = PaymentPlan
        fields = ['name', 'plan_type', 'price_min', 'price_max']

class PaymentMethodFilter(filters.FilterSet):
    method_type = filters.ChoiceFilter(choices=PaymentMethod.PAYMENT_TYPES)
    is_verified = filters.BooleanFilter()
    is_default = filters.BooleanFilter()

    class Meta:
        model = PaymentMethod
        fields = ['method_type', 'is_verified', 'is_default']

class SubscriptionFilter(filters.FilterSet):
    plan = filters.ModelChoiceFilter(queryset=PaymentPlan.objects.all())
    status = filters.ChoiceFilter(choices=Subscription.STATUS_CHOICES)
    auto_renew = filters.BooleanFilter()
    start_date = filters.DateFilter()
    end_date = filters.DateFilter()

    class Meta:
        model = Subscription
        fields = ['plan', 'status', 'auto_renew', 'start_date', 'end_date']

class PaymentFilter(filters.FilterSet):
    subscription = filters.ModelChoiceFilter(queryset=Subscription.objects.all())
    method = filters.ModelChoiceFilter(queryset=PaymentMethod.objects.all())
    status = filters.ChoiceFilter(choices=Payment.STATUS_CHOICES)
    amount_min = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    date_min = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_max = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Payment
        fields = ['subscription', 'method', 'status', 'amount_min', 'amount_max', 'date_min', 'date_max']

class InvoiceFilter(filters.FilterSet):
    payment = filters.ModelChoiceFilter(queryset=Payment.objects.all())
    status = filters.ChoiceFilter(choices=Invoice.STATUS_CHOICES)
    amount_min = filters.NumberFilter(field_name='amount', lookup_expr='gte')
    amount_max = filters.NumberFilter(field_name='amount', lookup_expr='lte')
    date_min = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_max = filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Invoice
        fields = ['payment', 'status', 'amount_min', 'amount_max', 'date_min', 'date_max'] 