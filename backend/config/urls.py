from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
import views

urlpatterns = [
    path('', views.index, name='home'),

    path('', views.index, name='index'),
    path('users-list/', views.users_list, name='users_list'),

    # N-layer architecture endpoints
    path('api/users/', views.user_list_create, name='user_list_create'),
    path('api/users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('api/auth/verify-email/', views.verify_email, name='verify_email'),

    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
