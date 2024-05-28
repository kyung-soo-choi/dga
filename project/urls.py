from django.contrib import admin
from django.urls import include, path

# URL-Muster definieren
urlpatterns = [
    # Pfad für das Admin-Interface
    path('admin/', admin.site.urls),
    # Inkludieren der API-URLs
    path('api/', include('api.urls')),
]
