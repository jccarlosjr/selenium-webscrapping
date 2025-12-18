from django.urls import path
from .views import ScrapperView, ScrapperTemplateView

urlpatterns = [
    path("scrapper/", ScrapperView.as_view(), name="scrapper"),
    path("consulta/", ScrapperTemplateView.as_view(), name="consulta-cpf"),
]
