from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('author', 'post', 'text', 'id', 'created',)
        read_only_fields = ('post', 'created',)
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    following = SlugRelatedField(queryset=User.objects.all(),
                                 slug_field='username')
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following',)
