from django.contrib import admin
from django.urls import path

from feedback.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("live", live),
    path("answer/<uuid:id_>", answer),
    path("question/<str:key>", question),
    path("question/<str:key>/answer", question_answers),
    path("question/<str:key>/summary", summary),
]
