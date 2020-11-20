from django.urls import include, path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('ipl/', include('ipl.urls')),
    path('', TemplateView.as_view(template_name="home.html"), name="home")
]
