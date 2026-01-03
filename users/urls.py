from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import DefaultRouter
from users import views as web_api_views

router = DefaultRouter()

router.register("token", web_api_views.TokenObtainPairViewSet, basename="jwt")
router.register(
    "token/refresh", web_api_views.TokenRefreshViewSet, basename="jwt_refresh"
)
router.register(
    "token/clear", web_api_views.ClearTokenViewSet, basename="token_clear"
)

urlpatterns = [
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += router.urls
