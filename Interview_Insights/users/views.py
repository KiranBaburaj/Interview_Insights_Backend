# accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmployerSerializer, JobSeekerSerializer, RecruiterSerializer, SignupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
# accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignupSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import random

class SignupAndSendOTPView(APIView):
    authentication_classes = []  # Ensure no authentication is required
    permission_classes = []  # Ensure no permissions are required

    def post(self, request):
        # Log the request data
        print("Request Data:", request.data)

        # Extract data from the request
        user_data = request.data.get('user')
        role = request.data.get('role')

        # Validate input data
        if not user_data or not role:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        email = user_data.get('email')
        password = user_data.get('password')
        full_name = user_data.get('full_name')

        if not email or not password or not full_name:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate OTP
        otp = random.randint(100000, 999999)
        OTP.objects.create(email=email, otp=otp)

        try:
            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'your-email@gmail.com',  # Replace with your email
                [email],  # Ensure email is a list of strings
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save user data if OTP sending succeeds
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
            return Response({"message": "Signup successful and OTP sent"}, status=status.HTTP_201_CREATED)
        else:
            # If serializer validation fails, delete OTP and return error
            OTP.objects.filter(email=email).delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import CustomAuthTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, JobSeeker, Employer, Recruiter
from django.contrib.auth import authenticate
# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny  

class LoginView(APIView):
    permission_classes = [AllowAny]  # Ensure this is set to allow any user

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'accessToken': str(refresh.access_token),
                'refreshToken': str(refresh),
                'user': {
                    'email': user.email,
                    'full_name': user.full_name,
                    'id':user.id,
                },
                'role': 'jobseeker' if hasattr(user, 'jobseeker') else 'employer' if hasattr(user, 'employer') else 'recruiter' if hasattr(user, 'recruiter') else 'unknown'
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import User, OTP
from .serializers import UserSerializer
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import OTP
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTP

class VerifyOTPAndSignupView(APIView):
    authentication_classes = []  # Ensure no authentication is required
    permission_classes = []

    def post(self, request):
        # Log the request data
        print("Verify OTP Request Data:", request.data)

        # Extract OTP from the request
        otp_code = request.data.get('otp')

        # Validate input data
        if not otp_code:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = OTP.objects.get(otp=otp_code)
            
            # OTP is valid, delete it and return success response
            email = otp_record.email  # Capture the email before deleting the record
            otp_record.delete()
            return Response({
                "message": "OTP verified successfully",
                "email": email
            }, status=status.HTTP_200_OK)
        
        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        

# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

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
    
    # Logic specific to admin dashboard
    return Response({'message': 'Welcome to admin dashboard!', 'user': request.user.email})



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import JobSeeker, Employer, Recruiter
from .serializers import JobSeekerSerializer, EmployerSerializer, RecruiterSerializer

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


# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import User, OTP
from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer
import random

class RequestPasswordResetView(APIView):
    authentication_classes = []  # Ensure no authentication is required
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
                    'your-email@gmail.com',  # Replace with your email
                    [email],  # Ensure email is a list of strings
                    fail_silently=False,
                )
                return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    authentication_classes = []  # Ensure no authentication is required
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

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
