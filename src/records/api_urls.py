from rest_framework.routers import DefaultRouter
from records.api import EndocrinologyRecordViewSet, CardiologyRecordViewSet

router = DefaultRouter()
router.register(r'endocrinology', EndocrinologyRecordViewSet, basename='endocrinology')
router.register(r'cardiology', CardiologyRecordViewSet, basename='cardiology')

urlpatterns = router.urls
