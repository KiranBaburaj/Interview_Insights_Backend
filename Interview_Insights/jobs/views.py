
from rest_framework import viewsets, permissions, generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

# Importing models
from .models import Job, JobApplication, JobCategory, SavedJob, JobSkill
from users.models import JobSeeker

# Importing serializers
from .serializers import (
    JobSerializer, 
    JobApplicationSerializer, 
    JobCategorySerializer, 
    SavedJobSerializer, 
    JobApplicationStatusSerializer, 
    JobSkillSerializer
)

# Importing custom permissions
from .permissions import IsEmployerOwnerOrAdmin

# Importing filters
from .filters import JobFilter, JobApplicationFilter



class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    queryset = Job.objects.none()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'location']  # Add fields you want to search

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            queryset = Job.objects.filter(is_active=True)
        elif self.request.user.is_staff:
            queryset = Job.objects.all()
        elif not hasattr(self.request.user, 'employer'):
            queryset = Job.objects.none()
        else:
            queryset = Job.objects.filter(employer=self.request.user.employer, is_active=True)
        
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            serializer.save(employer=self.request.user.employer)
        else:
            serializer.save()


class JobSkillViewSet(viewsets.ModelViewSet):
    serializer_class = JobSkillSerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]

    queryset = JobSkill.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return JobSkill.objects.all()
        return JobSkill.objects.all()

    def perform_create(self, serializer):
        serializer.save()
class JobCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticated, IsEmployerOwnerOrAdmin]

    queryset = JobCategory.objects.none()

    def get_queryset(self):
        if self.request.user.is_staff:
            return JobCategory.objects.all()
        return JobCategory.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def perform_create(self, serializer):
        job_seeker = self.request.user.jobseeker
        serializer.save(job_seeker=job_seeker)

    def create(self, request, *args, **kwargs):
        use_profile_resume = request.data.get('use_profile_resume', 'false').lower() == 'true'
        print(f"use_profile_resume.data: {use_profile_resume}")
        
        # Debugging: Print the entire request data and files
        print(f"request.data: {request.data}")
        print(f"request.FILES: {request.FILES}")

        if use_profile_resume:
            # Use the resume from the user's profile
            resume = request.user.jobseeker.resume
            print(f"def resume: {resume}")
        else:
            # Use the custom resume uploaded in this request
            resume = request.FILES.get('resume')
            print(f"Uploaded resume: {resume}")

        if not resume:
            return Response({"resume": ["No resume was provided."]}, status=status.HTTP_400_BAD_REQUEST)

        # Copy request data and update resume
        data = request.data.copy()
        data['resume'] = resume

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Save with perform_create to ensure job_seeker is set
        self.perform_create(serializer)
        
        # Update the instance with the new resume
        if not use_profile_resume and 'resume' in request.FILES:
            job_application = serializer.instance
            job_application.resume = request.FILES['resume']
            job_application.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

      

class CheckApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        job_seeker = self.request.user.jobseeker
        has_applied = JobApplication.objects.filter(job_seeker=job_seeker, job_id=job_id).exists()
        return Response({'hasApplied': has_applied})


class UpdateApplicationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, job_id):
        try:
            application = JobApplication.objects.get(id=job_id)
        except JobApplication.DoesNotExist:
            return Response({'error': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user is the employer of the job or an admin
        if not request.user.is_staff and application.job.employer.user != request.user:
            return Response({'error': 'You do not have permission to update this application.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = JobApplicationStatusSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def job_applicants(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        applicants = JobApplication.objects.filter(job=job)
        serializer = JobApplicationSerializer(applicants, many=True)
        return Response(serializer.data)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=404)



class JobApplicationList(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobApplicationFilter  # Add the filterset class

    def get_queryset(self):
        user = self.request.user
        return JobApplication.objects.filter(job_seeker__user=user)
    

class SavedJobListView(generics.ListCreateAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(job_seeker=self.request.user.jobseeker)

    def perform_create(self, serializer):
        serializer.save(job_seeker=self.request.user.jobseeker)



class SavedJobDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(job_seeker=self.request.user.jobseeker)

    def get_object(self):
        # Retrieve the job_id from the URL
        job_id = self.kwargs.get('job_id')
        
        # Attempt to get the SavedJob instance for the given job_id and the current user's job_seeker
        try:
            saved_job = SavedJob.objects.get(job_id=job_id, job_seeker=self.request.user.jobseeker)
        except SavedJob.DoesNotExist:
            # If the SavedJob does not exist, raise a NotFound exception
            raise NotFound('Saved job not found for this user.')

        return saved_job

    def delete(self, request, *args, **kwargs):
        # Get the SavedJob instance
        self.object = self.get_object()
        
        # Perform the deletion
        self.object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

@api_view(['GET'])
def matching_jobseekers(request):
    job_id = request.query_params.get('job_id')
    if not job_id:
        return Response({"error": "Job ID is required"}, status=400)

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=404)

    # Create a query to find matching job seekers
    matching_seekers = JobSeeker.objects.filter(
        Q(skills__skill_name__in=job.skills_required.all()) |
        Q(work_experience__job_title__icontains=job.title) |
        Q(educations__field_of_study__icontains=job.job_function)
    ).distinct()

    serializer = JobSeekerSerializer(matching_seekers, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matching_jobs(request):
    job_seeker = request.user.jobseeker
    
    # Get the job seeker's skills
    job_seeker_skills = job_seeker.skills.all()
    job_seeker_work_experience=job_seeker.work_experience.all()
    
    # Convert JobSkill objects to their names
    job_seeker_skill_names = job_seeker_skills.values_list('skill_name', flat=True)
    print(job_seeker_skill_names)
    job_seeker_EXPERIENCE_names= job_seeker_work_experience.values_list('job_title',flat=True)
    print(job_seeker_EXPERIENCE_names)
    print("currjob ",job_seeker.current_job_title)
    print(job_seeker.current_job_title)

    # Find matching jobs
    matching_jobs = Job.objects.filter(
        (Q(skills_required__name__in=job_seeker_skill_names) |
        Q(job_function__icontains=job_seeker.current_job_title) |
         Q(experience_level__icontains=job_seeker.current_job_title)|
        Q(title__icontains=job_seeker_EXPERIENCE_names))&
        Q(status='open') 
    ).distinct()

    serializer = JobSerializer(matching_jobs, many=True)
    return Response(serializer.data)
