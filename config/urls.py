# ELM API initialization
from django.urls import path, include

from modules.elm.api import urls as elm_urls

urlpatterns = [
    path('v1/elm/', include(elm_urls)),
]