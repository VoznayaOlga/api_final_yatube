from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)
from posts.models import Comment, Follow, Group, Post, User


class BaseModelViewSet(viewsets.ModelViewSet):
    pagination_class = None
    permission_classes = (IsAuthorOrReadOnly,)


class PostViewSet(BaseModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if 'limit' not in self.request.query_params:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
    permission_classes = (IsAuthorOrReadOnly,)


class CommentViewSet(BaseModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.get_post())

    def perform_update(self, serializer):
        serializer.save(post=self.get_post())


class FollowViewSet(BaseModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data,
                                           context={'user': user})
        if serializer.is_valid():
            following = User.objects.get(username=request.data['following'])
            if following == self.request.user:
                return Response(data={'following':
                                      ['Нельзя подписаться на самого себя']},
                                status=status.HTTP_400_BAD_REQUEST)
            elif (Follow.objects.
                  filter(user=self.request.user,
                         following=following).count() > 0):
                return Response(data={'following':
                                      ['Такая подписка уже есть']},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=self.request.user)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
