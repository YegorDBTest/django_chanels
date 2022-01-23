from django.conf.urls import include
from django.urls import path
from django.contrib import admin

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),

    path('api/jwt/token/', TokenObtainPairView.as_view(), name='jwt_token_obtain_pair'),
    path('api/jwt/token/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
]
