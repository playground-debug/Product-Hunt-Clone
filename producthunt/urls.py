from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('accounts/', include('account.urls'), name='accounts'),
    path('products/', include('product.urls'), name='products')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)