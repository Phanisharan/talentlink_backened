from rest_framework import generics
from .models import Job
from .serializers import JobSerializer
from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer

class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer


    def get_queryset(self):
        cached_jobs = cache.get("jobs_list")
        if cached_jobs:
            return Job.objects.filter(id__in=[job["id"] for job in cached_jobs])  

        jobs = Job.objects.all().order_by('-posted_at')
        serialized_jobs = JobSerializer(jobs, many=True).data  
        cache.set("jobs_list", serialized_jobs, timeout=60 * 5)  
        return jobs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = JobSerializer(queryset, many=True).data
        return Response(serialized_data)

    def perform_create(self, serializer):
        job = serializer.save()
        cache.delete("jobs_list")  
        return job


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def retrieve(self, request, *args, **kwargs):
        job_id = self.kwargs.get('pk')
        cache_key = f"job_{job_id}" 

        cached_job = cache.get(cache_key)
        if cached_job:
            return Response(cached_job) 
        
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 10)  
        return response

    def perform_update(self, serializer):
        job = serializer.save()
        cache.delete(f"job_{job.id}") 
        cache.delete("jobs_list") 
        return job

    def perform_destroy(self, instance):
        cache.delete(f"job_{instance.id}")  
        cache.delete("jobs_list") 
        instance.delete()
