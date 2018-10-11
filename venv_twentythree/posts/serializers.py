from rest_framework import serializers
from .models import MakePost
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField
from comments.serializers import CommentListSerializer
from comments.models import Comment


class PostListSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='posts:api_detail', lookup_field='pk')
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = MakePost
        fields = ('id', 'author', 'title', 'created_date', 'url')


class PostDetailSerializer(serializers.ModelSerializer):
    delete_url = HyperlinkedIdentityField(view_name='posts:api_delete', lookup_field='pk')
    author = serializers.StringRelatedField(many=False)
    image = SerializerMethodField()
    comments = SerializerMethodField()

    class Meta:
        model = MakePost
        fields = ('id', 'author', 'title', 'info', 'created_date', 'delete_url', 'image', 'comments')

    def get_image(self, obj):  # if a post has an image show the url
        try:
            image = obj.post_pic.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        object_id = obj.id
        c_qs = Comment.objects.filter(post=object_id)
        comments = CommentListSerializer(c_qs, many=True).data
        return comments


class PostUpdateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = MakePost
        fields = ('author', 'title', 'info', 'post_pic')


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = MakePost
        fields = ('author', 'title', 'info', 'post_pic')