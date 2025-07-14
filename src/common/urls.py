from django.urls import path
from common.views import HomeView, AboutView, ContactView, PrivacyPolicyView, DashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('privacy/', PrivacyPolicyView.as_view(), name='privacy'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

]
