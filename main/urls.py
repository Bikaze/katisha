from rest_framework import routers
from .views import TicketTemplateViewSet

router = routers.DefaultRouter()
router.register('tickets', TicketTemplateViewSet)

urlpatterns = router.urls