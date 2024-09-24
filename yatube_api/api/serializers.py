from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

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


class CurrentUserDefault():
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['request'].user


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username', default=CurrentUserDefault())
    following = SlugRelatedField(queryset=User.objects.all(),
                                 slug_field='username')

    class Meta:
        model = Follow
        fields = ('following', 'user')
        read_only_fields = ('user',)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]

    def validate_following(self, value):
        if (self.context['request'].user.username
                == self.initial_data['following']):
            raise serializers.ValidationError('Нельзя подписаться '
                                              'на самого себя')
        return value
