from django.urls import path
from .views import ChartTableView

urlpatterns = [
    path('table/', ChartTableView.as_view(), name='chart_table'),
]
