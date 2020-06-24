import requests, os

from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from common.generate_form_data import encode_multipart_formdata

from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404

from users.constants import GET_ROLE_TYPE
from users.models import SocialLink

from utilities.models import Branch, Website

from users.serializers import (
    StudentSerializer,
    CompanySerializer,
    PersonSerializer,
    RegisterSerializer
)

from users.models import (
    Student,
    Person,
    Company
)


class BasicUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = PersonSerializer
    queryset = Person.objects.all()

    def get_object(self):
        return get_object_or_404(Person, pk=self.request.user.pk)


class AvatarUploadAPI(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        user = request.user
        profile_image = request.data.get('profile_image') or None

        if profile_image:
            user.profile_image = profile_image
            user.save()
            return Response(PersonSerializer(user).data , status=status.HTTP_200_OK)
        else:
            return Response({'error_message': 'Profile image not found'}, status=status.HTTP_400_BAD_REQUEST)
        

class SelfProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        person = self.request.user
        role_type = self.request.user.role_type

        if role_type == GET_ROLE_TYPE.STUDENT:
            queryset = Student.objects.get(person=person)
        elif role_type == GET_ROLE_TYPE.COMPANY:
            queryset = Company.objects.get(person=person)
        else:
            queryset = None
        return queryset

    def get_serializer_class(self):
        if self.request.user.role_type == GET_ROLE_TYPE.STUDENT:
            return StudentSerializer
        elif self.request.user.role_type == GET_ROLE_TYPE.COMPANY:
            return CompanySerializer
        else:
            return None

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        if user.student_profile:
            user_profile = user.student_profile

            first_name = data.get('first_name') or None
            last_name = data.get('last_name') or None
            branch = data.get('branch') or None
            phone_number =  data.get('phone_number') or None
            enrollment_number = data.get('enrollment_number') or None
            course = data.get('course') or None
            year = data.get('year') or None
            social_links = data.get('social_links') or None
            interest = data.get('interest') or None
            bio = data.get('bio') or None
            achievements = data.get('achievements') or None
            availability_status = data.get('availability_status') or None

            if first_name:
                first_name = first_name.strip()
                user_profile.first_name = first_name

            if last_name:
                last_name = last_name.strip()
                user_profile.last_name = last_name

            if phone_number:
                phone_number = phone_number.strip()
                user_profile.phone_number = phone_number

            if branch:
                try:
                    branch = get_object_or_404(Branch, name=branch)
                except Branch.DoesNotExist:
                    return Response({'error_message': 'Branch not found'}, status=status.HTTP_400_BAD_REQUEST)
                user_profile.branch = branch
            
            if enrollment_number:
                enrollment_number = enrollment_number.strip()
                user_profile.enrollment_number = enrollment_number
            
            if course:
                course = course.strip()
                user_profile.course = course
            
            if year:
                year = year.strip()
                user_profile.year = year
            
            if social_links:
                for social_link in social_links:
                    website = get_object_or_404(Website, name=social_link.get('website_name') or None)
                    profile_url = social_link.get('profile_url') or None
                    if profile_url:
                        if user_profile.social_links.filter(profile_url=profile_url, website=website).exists():
                            return Response({'error_message': 'Already profile added for %s' % (website.name)}, status=status.HTTP_400_BAD_REQUEST)
                        
                        user_profile.social_links.create(website=website, profile_url=profile_url)
                    else:
                        return Response({'error_message': 'Profile url not found for %s!' % (website.name)}, status=status.HTTP_400_BAD_REQUEST)

            if interest:
                interest = interest.strip()
                user_profile.interest = interest
                        
            if bio:
                bio = bio.strip()
                user_profile.bio = bio

            if achievements:
                achievements = achievements.strip()
                user_profile.achievements = achievements      

            if availability_status:
                if availability_status == 'active':
                    user_profile.availability_status = True
                else:
                    user_profile.availability_status = False

            user_profile.save()

            return Response(StudentSerializer(user_profile).data ,status=status.HTTP_200_OK)

        elif user.company_profile:
            user_profile = user.company_profile

            company_domain = data.get('availability_status') or None
            phone_number = data.get('availability_status') or None
            category_of_company = data.get('availability_status') or None
            team_size = data.get('availability_status') or None
            address = data.get('availability_status') or None

            if company_domain:
                company_domain = company_domain.strip()
                user_profile.company_domain = company_domain  

            if phone_number:
                phone_number = phone_number.strip()
                user_profile.phone_number = phone_number  
            
            if category_of_company:
                category_of_company = category_of_company.strip()
                user_profile.category_of_company = category_of_company  
            
            if team_size:
                team_size = team_size.strip()
                user_profile.team_size = team_size  
            
            if address:
                address = address.strip()
                user_profile.address = address  
            
            user_profile.save()
            
            return Response(status=status.HTTP_200_OK)


class ChanneliOAuthAPI(APIView):
    permission_classes = [AllowAny, ]

    @staticmethod
    def post(request, *args, **kwargs):
        code = request.data.get('code') or None

        if code:
            token_url = 'https://internet.channeli.in/open_auth/token/'
            files = {
                'client_id': os.getenv('CHANNELI_CLIENT_ID'),
                'client_secret': os.getenv('CHANNELI_CLIENT_SECRET'),
                'grant_type': os.getenv('CHANNELI_GRANT_TYPE'),
                'redirect_url': os.getenv('CHANNELI_REDIRECT_URL'),
                'code': code
            }
            encoded_data, content_type = encode_multipart_formdata(files)
            headers = {
                'Content-Type': content_type
            }
            response_data = requests.post(url=token_url, data=encoded_data, headers=headers)
            if 'json' in response_data.headers.get('Content-Type'):
                access_token = response_data.json().get('access_token') or None
                if access_token:
                    user_data_url = 'https://internet.channeli.in/open_auth/get_user_data/'
                    fetch_user_headers = {
                        'Authorization': 'Bearer %s' % access_token
                    }
                    get_user_data = requests.get(url=user_data_url, headers=fetch_user_headers)
                    if 'json' in get_user_data.headers.get('Content-Type'):
                        get_user_body = get_user_data.json()

                        student = get_user_body.get('student') or None
                        contact_information = get_user_body.get('contactInformation') or None
                        person_info = get_user_body.get('person') or None
                        biological_information = get_user_body.get('biologicalInformation') or None

                        username = student.get('enrolmentNumber') or None
                        email = contact_information.get('emailAddress') or None
                        if username:
                            try:
                                user = Person.objects.get(username=username)
                            except:
                                user = None
                            if user is None:
                                user = Person.objects.create(username=username, email=email,
                                                             role_type=GET_ROLE_TYPE.STUDENT, is_channeli_oauth=True)
                                profile_image = person_info.get('displayPicture') or None
                                if profile_image:
                                    user.profile_image = profile_image
                                user.save()

                                student_profile = Student.objects.create(person=user)

                                full_name = person_info.get('fullName') or None
                                phone_number = contact_information.get('primaryPhoneNumber') or None
                                enrollment_number = username
                                branch_name = student.get('branch name') or None
                                current_year = student.get('currentYear') or None
                                date_of_birth = biological_information.get('dateOfBirth') or None

                                if full_name:
                                    temp_arr = full_name.split(" ", 1)
                                    student_profile.first_name = temp_arr[0]
                                    student_profile.last_name = temp_arr[1]

                                if phone_number:
                                    student_profile.phone_number = phone_number

                                if enrollment_number:
                                    student_profile.enrollment_number = enrollment_number

                                if current_year:
                                    student_profile.current_year = current_year

                                if date_of_birth:
                                    student_profile.date_of_birth = date_of_birth

                                if branch_name:
                                    branch, branch_created = Branch.objects.get_or_create(name=branch_name)
                                    student_profile.branch = branch
                                student_profile.save()

                            token, created = Token.objects.get_or_create(user=user)
                            update_last_login(None, user)
                            return Response({'token': token.key, 'role': user.role_type}, status=status.HTTP_200_OK)
                        else:
                            return Response({'error_message': 'Username doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error_message': 'Invalid access token'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error_message': 'Invalid code type'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_message': 'OAuth code is missing!'}, status=status.HTTP_400_BAD_REQUEST)