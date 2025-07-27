from django.urls import path
from .views import (
    CardiologyRecordCreateView,
    CardiologyRecordListView,
    CardiologyRecordUpdateView,
    CardiologyRecordDeleteView,

    EndocrinologyRecordCreateView,
    EndocrinologyRecordListView,
    EndocrinologyRecordUpdateView,
    EndocrinologyRecordDeleteView,
)


urlpatterns = [
    # Cardiology
    path('cardiology/', CardiologyRecordListView.as_view(), name='cardiology_records_list'),
    path('cardiology/add/', CardiologyRecordCreateView.as_view(), name='add_cardiology_record'),
    path('cardiology/<int:pk>/edit/', CardiologyRecordUpdateView.as_view(), name='edit_cardiology_record'),
    path('cardiology/<int:pk>/delete/', CardiologyRecordDeleteView.as_view(), name='delete_cardiology_record'),

    # Endocrinology
    path('endocrinology/', EndocrinologyRecordListView.as_view(), name='endocrinology_records_list'),
    path('endocrinology/add/', EndocrinologyRecordCreateView.as_view(), name='add_endocrinology_record'),
    path('endocrinology/<int:pk>/edit/', EndocrinologyRecordUpdateView.as_view(), name='edit_endocrinology_record'),
    path('endocrinology/<int:pk>/delete/', EndocrinologyRecordDeleteView.as_view(), name='delete_endocrinology_record'),
]
