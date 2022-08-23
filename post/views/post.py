import json
import datetime

from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware

from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics

from common.field_choices import get_duration_value
from post.constants import POST_TYPE
from post.serializers import (
    CompetitionSerializer,
    InternshipSerializer,
    ProjectSerializer
)
from post.serializers.applicants.internship import InternMinimumSerializer
from post.serializers.applicants.competition import CompetitionMinimumSerializer
from post.serializers.applicants.project import ProjectMinimumSerializer
from post.models import (
    Project,
    Competition,
    Internship,
    AppliedPostEntries,
)
from utilities.models import Location, Skill, Tag
from post.permissions import IsStudent


class PostBaseView(views.APIView):
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        user = request.user
        post_slug = self.kwargs.get('slug') or None

        try:
            if user.student_profile:
                user_profile = user.student_profile
            elif user.company_profile:
                user_profile = user.company_profile
            else:
                user_profile = user.person_profile
        except:
            return None

        request.post = None
        if post_slug:
            try:
                request.post = Internship.objects.get(slug=post_slug)
                request.post_type = POST_TYPE.INTERNSHIP_POST_TYPE
            except:
                pass
            try:
                request.post = Project.objects.get(slug=post_slug)
                request.post_type = POST_TYPE.COMPETITION_POST_TYPE
            except:
                pass
            try:
                request.post = Competition.objects.get(slug=post_slug)
                request.post_type = POST_TYPE.PROJECT_POST_TYPE
            except:
                pass

        if request.post is None:
            request.post_type = None
        request.user_profile = user_profile


class PostViewSet(PostBaseView, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs['slug']

        if self.action in ['retrieve', 'update']:
            if Internship.objects.filter(slug=slug):
                return Internship.objects.filter(
                    slug=slug
                )
            if Project.objects.filter(slug=slug):
                return Project.objects.filter(
                    slug=slug
                )
            if Competition.objects.filter(slug=slug):
                return Competition.objects.filter(
                    slug=slug
                )

            return Response({"error_message": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        slug = self.kwargs['slug']

        if self.action in ['retrieve', 'update']:

            if Internship.objects.filter(slug=slug):
                return InternshipSerializer

            if Project.objects.filter(slug=slug):
                return ProjectSerializer

            if Competition.objects.filter(slug=slug):
                return CompetitionSerializer

            return Response(
                {
                    "error_message": 'Slug doesn\'t exists'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request, *args, **kwargs):
        post_type = request.GET.get('post_type') or None
        my_post = request.GET.get('my_post') or False
        user_id = request.GET.get('user_id') or False
        expired_post = request.GET.get('expired_post') or False
        unpublished_post = request.GET.get('unpublished_post') or False
        expired_my_post = request.GET.get('expired_my_post') or False
        unpublished_my_post = request.GET.get('unpublished_my_post') or False
        bookmark = request.GET.get('bookmark') or False
        applied_posts = request.GET.get('applied_posts') or False
        duration_unit = request.GET.get('duration_unit') or 0
        duration_value_ll = request.GET.get('duration_value_ll') or None
        duration_value_ul = request.GET.get('duration_value_ul') or None
        stipend_ll = request.GET.get('stipend_ll') or None
        stipend_ul = request.GET.get('stipend_ul') or None
        tag_hash = request.GET.getlist('tag_hash') or None
        location = request.GET.get('location') or None
        skill_slug = request.GET.getlist('skill_slug') or None
        now = timezone.now()

        if (duration_unit and duration_value_ll is None and duration_value_ul is None) or (duration_unit is None and (duration_value_ll or duration_value_ul)):
            return Response({"error_message": 'Duration param doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
        data = []

        if post_type:
            if int(post_type) == POST_TYPE.INTERNSHIP_POST_TYPE:  
                internships_queryset = Internship.objects.filter(is_verified=True, is_published=True,
                                                                 post_expiry_date__gte=now, ).exclude(user=request.user)\
                    .order_by('-updated_at')
                if my_post:
                    internships_queryset = Internship.objects.filter(user=request.user, is_published=True,
                                                                     post_expiry_date__gte=now)\
                        .order_by('-updated_at')
                if user_id:
                    internships_queryset = Internship.objects.filter(user__id=user_id, is_published=True,
                                                                     post_expiry_date__gte=now)\
                        .order_by('-updated_at')
                if expired_my_post:
                    internships_queryset = Internship.objects.filter(user=request.user, post_expiry_date__lte=now)\
                        .order_by('-updated_at')
                if expired_post:
                    internships_queryset = Internship.objects.filter(post_expiry_date__lte=now)\
                        .order_by('-updated_at')
                if unpublished_my_post:
                    internships_queryset = Internship.objects.filter(user=request.user, is_published=False, post_expiry_date__gte=now)\
                        .order_by('-updated_at')
                if unpublished_post:
                    internships_queryset = Internship.objects.filter(is_published=False, post_expiry_date__gte=now)\
                        .order_by('-updated_at')
                if bookmark:
                    internships_queryset = internships_queryset.filter(
                        bookmarks__person=request.user)
                if applied_posts:
                    post_ids = AppliedPostEntries.objects.filter(user_object_id=request.user_profile.id)\
                        .values_list('post_object_id', flat=True).distinct()
                    internships_queryset = internships_queryset.filter(
                        id__in=post_ids)
                if stipend_ll:
                    internships_queryset = internships_queryset.filter(
                        stipend__gte=int(stipend_ll))
                if stipend_ul:
                    internships_queryset = internships_queryset.filter(
                        stipend__lte=int(stipend_ul))
                if duration_unit:
                    value = get_duration_value(duration_unit)
                    if duration_value_ll:
                        internships_queryset = internships_queryset.filter(
                            duration_value__gte=int(duration_value_ll)*value)
                    if duration_value_ul:
                        internships_queryset = internships_queryset.filter(
                            duration_value__lte=int(duration_value_ul)*value)
                if location:
                    internships_queryset = internships_queryset.filter(
                        location__slug=location)
                if tag_hash:
                    internships_queryset = internships_queryset.filter(
                        tags__hash__in=tag_hash)
                if skill_slug:
                    internships_queryset = internships_queryset.filter(
                        required_skills__slug__in=skill_slug)

                data = InternshipSerializer(
                    internships_queryset,
                    context={'request': request},
                    many=True
                ).data

            elif int(post_type) == POST_TYPE.PROJECT_POST_TYPE:
                data = ProjectSerializer(
                    Project.objects.filter(
                        is_verified=True, is_published=True, post_expiry_date__gte=now)
                    .order_by('-created_at'),
                    context={'request': request},
                    many=True
                ).data

            elif int(post_type) == POST_TYPE.COMPETITION_POST_TYPE:
               
                data = CompetitionSerializer(
                    Competition.objects.filter(
                        is_verified=True, is_published=True, post_expiry_date__gte=now)
                    .order_by('-created_at'),
                    context={'request': request},
                    many=True
                ).data

            return Response(data, status=status.HTTP_200_OK)
        return Response({"error_message": 'Post type param doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, slug=None, **kwargs):
        user = request.user
        post = request.post
        post_type = request.post_type
        now = timezone.now()
        body = json.loads(request.body)

        if post is not None:
            if post.user == user:
                title = body.get('title') or None
                stipend = body.get('stipend') or None
                stipend_max = body.get('stipend_max') or None
                description = body.get('description') or None
                expiry_timestamp = body.get('expiry_timestamp') or None
                skill_slugs = body.get('skill_slugs') or None
                tag_hashes = body.get('tag_hashes') or None
                is_published = body.get('is_publish') or False
                data = {}
                if post_type == POST_TYPE.INTERNSHIP_POST_TYPE:
                    location = body.get('location') or None
                    duration_value = body.get('duration_value') or None
                    duration_unit = body.get('duration_unit') or None
                    if title:
                        post.title = title
                    if stipend:
                        post.stipend = stipend
                    if stipend_max:
                        post.stipend_max = stipend_max
                    if description:
                        post.description = description
                    if location:
                        try:
                            check_location = Location.objects.get(
                                slug=location)
                        except:
                            return Response({"error_message": 'Location doesn\'t exists'},
                                            status=status.HTTP_400_BAD_REQUEST)
                        if check_location:
                            post.location = check_location
                    if expiry_timestamp:
                        if datetime.datetime.fromtimestamp(expiry_timestamp) > datetime.datetime.now():
                            post.post_expiry_date = make_aware(
                                datetime.datetime.fromtimestamp(expiry_timestamp))
                        else:
                            return Response({"error_message": 'Expiry date cannot be less than current timestamp'},
                                            status=status.HTTP_400_BAD_REQUEST)
                    if duration_value and duration_unit and int(duration_value) > 1:
                        value = get_duration_value(duration_unit)
                        post.duration_value = int(duration_value) * value
                    if skill_slugs:
                        temp_slugs = []
                        for slug in skill_slugs:
                            try:
                                check_slug = Skill.objects.get(slug=slug)
                            except:
                                return Response({"error_message": 'Skill slug doesn\'t exists'},
                                                status=status.HTTP_400_BAD_REQUEST)
                            if check_slug:
                                temp_slugs.append(check_slug)
                        post.required_skills.set(temp_slugs)
                    if tag_hashes:
                        temp_hashes = []
                        for hash in tag_hashes:
                            try:
                                check_hash = Tag.objects.get(hash=hash)
                            except:
                                return Response({"error_message": 'Tag hash doesn\'t exists'},
                                                status=status.HTTP_400_BAD_REQUEST)
                            if check_hash:
                                temp_hashes.append(check_hash)
                        post.tags.set(temp_hashes)
                    if is_published:
                        post.is_published = True
                    else:
                        post.is_published = False
                    post.save()
                    data = InternshipSerializer(
                        post, context={'request': request},).data
                elif post_type == POST_TYPE.COMPETITION_POST_TYPE:
                   
                    data = CompetitionSerializer(
                        post, context={'request': request},).data

                elif post_type == POST_TYPE.PROJECT_POST_TYPE:
                    data = ProjectSerializer(
                        post, context={'request': request},).data

                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({"error_message": 'Not allowed to edit this post!'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error_message": 'Post slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, slug=None, **kwargs):
        user = request.user
        post = request.post

        if post is not None:
            if post.user == user:
                post.delete()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"error_message": 'Not allowed to delete this post!'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error_message": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)


class CreatePost(generics.CreateAPIView):

    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        post_type = self.request.data.get('post_type')

        if post_type == 'internship':
            return InternshipSerializer
        elif post_type == 'project':
            return ProjectSerializer
        elif post_type == 'competition':
            return CompetitionSerializer

        return None

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        post_type = data.get('post_type') or None

        if post_type:
            if int(post_type) in [POST_TYPE.INTERNSHIP_POST_TYPE, POST_TYPE.COMPETITION_POST_TYPE,
                             POST_TYPE.PROJECT_POST_TYPE]:
                title = data.get('title') or None
                description = data.get('description') or None
                expiry_timestamp = data.get('expiry_timestamp') or None
                skill_slugs = data.get('skill_slugs') or None
                tag_hashes = data.get('tag_hashes') or None
                is_published = data.get('is_publish') or False

                if expiry_timestamp:
                    if datetime.datetime.fromtimestamp(expiry_timestamp) <= datetime.datetime.now():
                        return Response({"error_message": 'Expiry date cannot be less than current timestamp'},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error_message": 'Expiry date is required'}, status=status.HTTP_400_BAD_REQUEST)

                if post_type == POST_TYPE.INTERNSHIP_POST_TYPE:
                    stipend = data.get('stipend') or None
                    stipend_max = data.get('stipend_max') or None
                    location = data.get('location') or None
                    duration_value = data.get('duration_value') or None
                    duration_unit = data.get('duration_unit') or None
                    internship = Internship.objects.create(user=user, post_expiry_date=make_aware(
                        datetime.datetime.fromtimestamp(expiry_timestamp)))
                    if title:
                        internship.title = title
                    if stipend:
                        internship.stipend = stipend
                    if stipend_max:
                        internship.stipend_max = stipend_max
                    if description:
                        internship.description = description
                    if location:
                        try:
                            check_location = Location.objects.get(
                                slug=location)
                        except:
                            return Response({"error_message": 'Location doesn\'t exists'},
                                            status=status.HTTP_400_BAD_REQUEST)
                        if check_location:
                            internship.location = check_location

                    if duration_value and duration_unit and int(duration_value) > 1:
                        value = get_duration_value(duration_unit)
                        internship.duration_value = int(duration_value) * value
                    if skill_slugs:
                        temp_slugs = []
                        for slug in skill_slugs:
                            try:
                                check_slug = Skill.objects.get(slug=slug)
                            except:
                                return Response({"error_message": 'Skill slug doesn\'t exists'},
                                                status=status.HTTP_400_BAD_REQUEST)
                            if check_slug:
                                temp_slugs.append(check_slug)
                        internship.required_skills.set(temp_slugs)
                    if tag_hashes:
                        temp_hashes = []
                        for hash in tag_hashes:
                            try:
                                check_hash = Tag.objects.get(hash=hash)
                            except:
                                return Response({"error_message": 'Tag hash doesn\'t exists'},
                                                status=status.HTTP_400_BAD_REQUEST)
                            if check_hash:
                                temp_hashes.append(check_hash)
                        internship.tags.set(temp_hashes)
                    if is_published:
                        internship.is_published = True
                    else:
                        internship.is_published = False
                    internship.save()

                    serializer_data = InternshipSerializer(
                        internship, context={'request': request}, ).data
                elif post_type == POST_TYPE.COMPETITION_POST_TYPE:
                    competition = Competition.objects.create(user=user, post_expiry_date=make_aware(
                        datetime.datetime.fromtimestamp(expiry_timestamp)))
                    serializer_data = CompetitionSerializer(
                        competition, context={'request': request}, ).data

                elif post_type == POST_TYPE.PROJECT_POST_TYPE:
                    project = Project.objects.create(user=user, post_expiry_date=make_aware(
                        datetime.datetime.fromtimestamp(expiry_timestamp)))
                    serializer_data = ProjectSerializer(
                        project, context={'request': request}, ).data

                return Response(
                    serializer_data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response({'error_message': 'post_type field value is incorrect'},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error_message': 'post_type field required'}, status=status.HTTP_400_BAD_REQUEST)


class ApplyPostView(PostBaseView):
    permission_classes = [IsAuthenticated, IsStudent]

    @staticmethod
    def check_post_object(slug):
        if Internship.objects.filter(slug=slug).exists():
            return Internship.objects.get(slug=slug)

        elif Project.objects.filter(slug=slug).exists():
            return Project.objects.get(slug=slug)

        elif Competition.objects.filter(slug=slug).exists():
            return Competition.objects.get(slug=slug)

        return None

    def post(self, request, *args, **kwargs):
        user_profile = request.user_profile
        post_slug = self.kwargs['slug']

        post = self.check_post_object(post_slug)

        if post:
            if post.applied_post_entries.filter(user_object_id=user_profile.id).exists():
                return Response({"error_message": 'Already applied to the post!'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                AppliedPostEntries.objects.create(user=user_profile, post=post)
                return Response(status=status.HTTP_200_OK)
            except:
                return Response({"error_message": 'Unable to apply'}, status=status.HTTP_403_FORBIDDEN)

        return Response({"error_message": 'Slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)


class ApplicantsPostView(PostBaseView, viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, ]
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        post_type = request.GET.get('post_type') or None
        obj = None
        data = None
        if slug:
            if post_type:
                if int(post_type) == POST_TYPE.INTERNSHIP_POST_TYPE:
                    internships_queryset = Internship.objects.filter(
                        user=request.user, slug=slug)

                    data = InternMinimumSerializer(
                        internships_queryset,
                        context={'request': request},
                        many=True
                    ).data

                elif int(post_type) == POST_TYPE.COMPETITION_POST_TYPE:
                    competition_queryset = Competition.objects.filter(
                        user=request.user, slug=slug)

                    data = CompetitionMinimumSerializer(
                        competition_queryset,
                        context={'request': request},
                        many=True
                    ).data

                elif int(post_type) == POST_TYPE.PROJECT_POST_TYPE:
                    project_queryset = Project.objects.filter(
                        user=request.user, slug=slug)

                    data = ProjectMinimumSerializer(
                        project_queryset,
                        context={'request': request},
                        many=True
                    ).data

                if data:
                    obj = data[0]
                    return Response(obj, status=status.HTTP_200_OK)
                else:
                    return Response({"error_message": 'param or slug doesn\'t match'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error_message": 'Post type param doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error_message": 'slug doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)
