from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from APP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('APP.urls')),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)