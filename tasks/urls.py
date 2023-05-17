from django.urls import include, path
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from tasks import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"tasks", views.TaskView, "tasks")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/tu-ruta-en-django/", views.YourView.as_view(), name="tu-nombre-de-ruta"),
    path('docs/', include_docs_urls(title='Tasks API')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

