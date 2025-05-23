"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("orders/", orders, name="orders"),
    path("admin/", admin.site.urls),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("accounts/", include("allauth.urls")),
    path("logout/", logout_confirm, name="logout_confirm"),  # Confirmation page
    path("logout-confirmed/", LogoutView.as_view(next_page="home"), name="logout"),
    path("menu/", include("menu.urls")),
    path("kitchen/", include("order.urls")),
    path('lunch/', include('lunch.urls')),
    # path("delete_order/<int:order_id>/", delete_order, name="cancel_order"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
