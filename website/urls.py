from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
#from patientPortal.views import Signup
#from patientPortal.views import information
#from patientPortal.views import myprogress

urlpatterns = [
    path('portal/', include('patientPortal.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
