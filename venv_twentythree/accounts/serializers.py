from rest_framework import serializers
from .models import Profile
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField
from posts.serializers import PostListSerializer
from posts.models import MakePost


class UsersListSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    url = HyperlinkedIdentityField(view_name='accounts:api_detail', lookup_field='pk')
    username = SerializerMethodField()
    first_name = SerializerMethodField()
    last_name = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'url')

    def get_first_name(self, obj):
        try:
            first_name = obj.user.first_name
        except:
            first_name = None
        return first_name

    def get_last_name(self, obj):
        try:
            last_name = obj.user.last_name
        except:
            last_name = None
        return last_name

    def get_username(self, obj):
        try:
            username = obj.user.username
        except:
            username = None
        return username


class UsersDetailSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=False)
    username = SerializerMethodField()
    first_name = SerializerMethodField()
    last_name = SerializerMethodField()
    profile_pic = SerializerMethodField()
    posts = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'gender', 'description', 'profile_pic', 'posts')

    def get_first_name(self, obj):
        try:
            first_name = obj.user.first_name
        except:
            first_name = None
        return first_name

    def get_last_name(self, obj):
        try:
            last_name = obj.user.last_name
        except:
            last_name = None
        return last_name

    def get_username(self, obj):
        try:
            username = obj.user.username
        except:
            username = None
        return username

    def get_profile_pic(self, obj):
        try:
            profile_pic = obj.profile_pic.url
        except:
            profile_pic = None
        return profile_pic

    def get_posts(self, obj):
        object_id = obj.user
        c_qs = MakePost.objects.filter(author=object_id)
        posts = PostListSerializer(c_qs, many=True, context=self.context).data
        return posts


class UserUpdateSerializer(serializers.ModelSerializer):
    # profile_pic = SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('description', 'profile_pic')

    # def update(self, instance, validated_data):
    #     instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
    #     return instance

    # def get_object(self):
    #     profile_pic = self.kwargs["profile_pic"]
    #     return get_object_or_404(Profile, profile_pic=profile_pic)