from django.urls import path

from scan import views

urlpatterns = [
    path('', views.ScanView.as_view(), name='root'),
    path(
        'dataField/<str:data_field>/trace_filtered',
        views.GetTraceFilteredView.as_view(),
        name='TraceFiltered',
    ),
    path(
        'dataField/<str:data_field>/stats_summary',
        views.GetStatsSummaryView.as_view(),
        name='StatsSummary',
    ),
]
