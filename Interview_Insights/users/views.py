from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
import random

from .models import User, OTP, JobSeeker, Employer, Recruiter
from .serializers import (
    UserSerializer, 
    SignupSerializer, 
    JobSeekerSerializer, 
    EmployerSerializer, 
    RecruiterSerializer, 
    PasswordResetSerializer, 
    PasswordResetConfirmSerializer,
    CustomAuthTokenSerializer
)

# Signup and Send OTP
class SignupAndSendOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        print("Request Data:", request.data)
        user_data = request.data.get('user')
        role = request.data.get('role')

        if not user_data or not role:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        email = user_data.get('email')
        password = user_data.get('password')
        full_name = user_data.get('full_name')

        if not email or not password or not full_name:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        otp = random.randint(100000, 999999)
        OTP.objects.create(email=email, otp=otp)

        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'your-email@gmail.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = {
            "user": {
                "email": email,
                "password": password,
                "full_name": full_name
            },
            "role": role
        }
        serializer = SignupSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            return Response({"message": "OTP sent", "user_id": user.id}, status=status.HTTP_201_CREATED)
        else:
            OTP.objects.filter(email=email).delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Debug: Print email and password received
        print(f"Login attempt with email: {email} and password: {password}")

        try:
            user = User.objects.get(email=email)

            # Debug: Print email verification status
            print(f"User found: {user.email}, Email Verified: {user.email_verified}")

            if not user.email_verified:
                return Response({'detail': 'Email not verified', "user_id": user.id}, status=status.HTTP_401_UNAUTHORIZED)

            user = authenticate(request, email=email, password=password)

            # Debug: Print authentication result
            print(f"Authentication attempt for user {email}: {'Success' if user else 'Failure'}")

            if user is not None:
                refresh = RefreshToken.for_user(user)
                role = 'jobseeker' if hasattr(user, 'jobseeker') else 'employer' if hasattr(user, 'employer') else 'recruiter' if hasattr(user, 'recruiter') else 'admin' if user.is_staff else 'unknown'

                # Debug: Print role
                print(f"User role: {role}")

                return Response({
                    'accessToken': str(refresh.access_token),
                    'refreshToken': str(refresh),
                    'user': {
                        'email': user.email,
                        'full_name': user.full_name,
                        'id': user.id,
                        
                    },
                    'role': role
                })
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            # Debug: Print message when user does not exist
            print(f"No user found with email: {email}")
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Verify OTP and Signup
class VerifyOTPAndSignupView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        print("Verify OTP Request Data:", request.data)

        otp_code = request.data.get('otp')

        if not otp_code:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = OTP.objects.get(otp=otp_code)

            if not otp_record.is_valid():
                return Response({"error": "OTP Incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            email = otp_record.email
            otp_record.delete()

            user, created = User.objects.get_or_create(email=email)
            user.email_verified = True
            user.is_active=True
            user.save()

            serializer = UserSerializer(user)
            return Response({
                "message": "OTP verified successfully",
                "user": serializer.data
            }, status=status.HTTP_200_OK)

        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


# Resend OTP
class ResendOTPView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
            email = user.email

            OTP.objects.filter(email=email).delete()

            otp = random.randint(100000, 999999)
            OTP.objects.create(email=email, otp=otp)

            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    'your-email@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"detail": "OTP resent successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Admin Login and Dashboard
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    
    if user is not None and user.is_superuser:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': 'admin',
            'user': {
                'email': user.email,
                'full_name': user.full_name
            }
        })
    return Response({'detail': 'Invalid credentials or not an admin'}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard(request):
    if not request.user.is_superuser:
        return Response({'detail': 'You do not have permission to access this resource.'}, status=403)
    
    return Response({'message': 'Welcome to admin dashboard!', 'user': request.user.email})


# List Job Seekers, Employers, and Recruiters
@api_view(['GET'])
@permission_classes([])
def list_jobseekers(request):
    jobseekers = JobSeeker.objects.all()
    serializer = JobSeekerSerializer(jobseekers, many=True)
    print("Job Seekers Data:", serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def list_employers(request):
    employers = Employer.objects.all()
    serializer = EmployerSerializer(employers, many=True)
    print("Employers Data:", serializer.data)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([])
def list_recruiters(request):
    recruiters = Recruiter.objects.all()
    serializer = RecruiterSerializer(recruiters, many=True)
    print("Recruiters Data:", serializer.data)
    return Response(serializer.data)


# Password Reset
class RequestPasswordResetView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                otp = random.randint(100000, 999999)
                OTP.objects.create(email=email, otp=otp)

                send_mail(
                    'Your Password Reset OTP',
                    f'Your OTP code is {otp}',
                    'your-email@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            print(f"Resetting password  {new_password}")

            try:
                otp_record = OTP.objects.get(email=email, otp=otp)
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                otp_record.delete()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            except OTP.DoesNotExist:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
