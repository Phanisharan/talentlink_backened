from django.urls import path
from .views import JobListCreateView, JobDetailView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
]
