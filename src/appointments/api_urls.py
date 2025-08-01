from rest_framework.routers import DefaultRouter
from appointments.api import AppointmentViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls
