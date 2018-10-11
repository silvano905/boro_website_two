from rest_framework import serializers
from .models import Comment
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField


class CommentListSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='comments:api_detail', lookup_field='pk')
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = ('post', 'author', 'url')


class CommentDetailSerializer(serializers.ModelSerializer):
    delete_url = HyperlinkedIdentityField(view_name='comments:api_delete', lookup_field='pk')
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created_date', 'delete_url')


class CommentUpdateSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = ('author', 'text',)