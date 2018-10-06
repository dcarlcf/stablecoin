from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'paxos-usd-request/', views.PaxosUSDRequest.as_view()),
]
