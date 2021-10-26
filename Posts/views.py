
from rest_framework import viewsets,permissions
from .serializers import PostsSerializer
from .models import Post
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


    @action(detail=True, methods=['patch'],permission_classes = [permissions.IsAuthenticatedOrReadOnly])
    def like(self, request, *args, **kwargs):
        Post = self.get_object()
        user = request.user
        if user not in Post.users_who_liked.all():
            likes = Post.likes
            likes += 1
            Post.likes = likes
            Post.users_who_liked.add(user)
            Post.save()

        serializer = self.get_serializer(Post)

        return Response(serializer.data)

    @action(detail=True, methods=['patch'],permission_classes = [permissions.IsAuthenticatedOrReadOnly])
    def unlike(self, request, *args, **kwargs):
        Post = self.get_object()
        user = request.user
        if user in Post.users_who_liked.all():
            likes = Post.likes
            likes -= 1
            Post.likes = likes
            Post.users_who_liked.remove(user)
            Post.save()

        serializer = self.get_serializer(Post)

        return Response(serializer.data)

    @action(detail=False,methods=['GET','HEAD',"OPTIONS"])
    def order_by_likes(self, request, *args, **kwargs):
        Posts = self.get_queryset()
        Posts = Posts.order_by('-likes')
        serializer = self.get_serializer(Posts,many=True)

        return Response(serializer.data)


    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    