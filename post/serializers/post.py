from rest_framework import serializers
from post.models.post import Post
from users.serializers.profile import ProfileViewSerializer


class Postserializer(serializers.ModelSerializer):
    author = ProfileViewSerializer(read_only=True)
    slug = serializers.SlugField(required=False)
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Post
        fields = (
            'author',
            'createdAt',
            'slug',
            'updatedAt',
            'company_name'
            'company_domain',
            'description',
            'work_location',
            'start_date',
            'completition_date',
            'post_expiry_date',
            'appicant_numbers',
            'competition_type',
            'work_type',
            'work_description',
            'stipend',
            'required_skill',
            'product_detail'
        )

    def create(self, validated_data):
        author = self.context.get('author', None)
        post = Post.objects.create(author=author, **validated_data)

        return post

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
