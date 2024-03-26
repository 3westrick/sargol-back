from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("__debug__/", include("debug_toolbar.urls")),

    # path("auth/", obtain_auth_token),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("adminpanel/", include('adminpanel.urls')),

    path("categories/", include('category.urls')),
    # path("products/", include('product.urls')),
    path("attributes/", include('attribute.urls')),
    path("values/", include('value.urls')),
    path("images/", include('images.urls')),



    path("", include('base.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

