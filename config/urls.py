
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),   
    path('userauth/', include('django.contrib.auth.urls')),    # built-in django auth
    path('userauth/', include('userauth.urls')),   
    path('accounts/', include('allauth.urls')),   
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)          # url path reference for created media



# Configure Admin Titles
admin.site.site_header = "Events-App Admin Page"
admin.site.site_title = "Browser Lookup"
admin.site.index_title = "Welcome To Admin Dashboard"

