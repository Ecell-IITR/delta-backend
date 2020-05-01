from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from users.constants import GET_ROLE_TYPE
from users.models import SocialLink

from utilities.models import Branch, Website

from users.serializers import (
    StudentSerializer,
    CompanySerializer,
    PersonSerializer
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
            social_link = data.get('social_link') or None
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
            
            if social_link:
                try:
                    website = get_object_or_404(Website, name=social_link.get('website_name') or None)
                except Website.DoesNotExist:
                    return Response({'error_message': 'Website not found'}, status=status.HTTP_400_BAD_REQUEST)
                
                profile_url = social_link.get('profile_url') or None
                
                if profile_url:
                    if user_profile.social_links.filter(profile_url=profile_url, website=website).exists():
                        return Response({'error_message': 'Already profile added for this website'}, status=status.HTTP_400_BAD_REQUEST)
                    
                    user_profile.social_links.create(website=website, profile_url=profile_url)

                else:
                    return Response({'error_message': 'Profile url not found!'}, status=status.HTTP_400_BAD_REQUEST)

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
                user_profile.availability_status = availability_status

            user_profile.save()

            return Response(status=status.HTTP_200_OK)

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