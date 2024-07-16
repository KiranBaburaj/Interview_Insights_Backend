# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import JobSeeker, Employer, Recruiter, Company

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name','id']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
        )
        return user

class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = JobSeeker
        fields = [ 'user','phone_number', 'date_of_birth', 'profile_photo_url', 'bio', 'linkedin_url', 'portfolio_url', 'resume_url', 'current_job_title', 'job_preferences']

class EmployerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employer
        fields = [ 'user','company', 'company_role']

class RecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Recruiter
        fields = ['id', 'user','company', 'recruiter_level']

class SignupSerializer(serializers.Serializer):
    user = UserSerializer()
    role = serializers.ChoiceField(choices=[('job_seeker', 'Job Seeker'), ('employer', 'Employer'), ('recruiter', 'Recruiter')])
    job_seeker = JobSeekerSerializer(required=False)
    employer = EmployerSerializer(required=False)
    recruiter = RecruiterSerializer(required=False)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        role = validated_data.pop('role')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)

        if role == 'job_seeker':
            JobSeeker.objects.create(user=user, **validated_data.get('job_seeker', {}))
        elif role == 'employer':
            Employer.objects.create(user=user, **validated_data.get('employer', {}))
        elif role == 'recruiter':
            Recruiter.objects.create(user=user, **validated_data.get('recruiter', {}))

        return user
# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
# users/serializers.py

from rest_framework import serializers
from .models import OTP

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'


# serializers.py

from rest_framework import serializers
from .models import User

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)


