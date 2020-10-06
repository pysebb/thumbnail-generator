from django.urls import path
from .views import IndexView, VideoView

urlpatterns = [
    path('', IndexView.as_view()),
    path('<int:pk>/', VideoView.as_view(), name='video-view'),
]
