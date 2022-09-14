"""my_first_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path

from products.views import index, products, as_favorite, buy_product, favorites, purchases
from users.views import register_user, login_view, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Index
    path("", index, name="index"),

    # Users
    path("register/", register_user, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Products
    path("products/", products, name="products"),
    path("products/<int:product_id>/as_favorite/", as_favorite, name="as_favorite"),
    path("products/<int:product_id>/buy/", buy_product, name="buy_product"),

    # Favorites
    path("products/favorites", favorites, name="favorites"),

    # Purchases
    path("products/purchases", purchases, name="purchases"),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
