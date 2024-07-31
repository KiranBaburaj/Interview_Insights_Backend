from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
import chat.routing  # Make sure this import is correct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include([
        path('', include('users.urls')),
        path('', include('employer.urls')),
        path('', include('jobs.urls')),
        path('jobseek/', include('jobseeker.urls')),
        path('', include('chat.urls')),
        path('', include('customadmin.urls')),
    ])),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
