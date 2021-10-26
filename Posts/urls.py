from django.urls import include, path
from rest_framework import routers
from .views import PostsViewSet

router = routers.DefaultRouter()
router.register(r'api', PostsViewSet)

app_name="Posts"
urlpatterns = [
    path('', include(router.urls)),
]
'''
posts/ ^api/$ [name='post-list']
posts/ ^api\.(?P<format>[a-z0-9]+)/?$ [name='post-list']
posts/ ^api/order_by_likes/$ [name='post-order-by-likes']
posts/ ^api/order_by_likes\.(?P<format>[a-z0-9]+)/?$ [name='post-order-by-likes']
posts/ ^api/(?P<pk>[^/.]+)/$ [name='post-detail']
posts/ ^api/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='post-detail']
posts/ ^api/(?P<pk>[^/.]+)/like/$ [name='post-like']
posts/ ^api/(?P<pk>[^/.]+)/like\.(?P<format>[a-z0-9]+)/?$ [name='post-like']
posts/ ^api/(?P<pk>[^/.]+)/unlike/$ [name='post-unlike']
posts/ ^api/(?P<pk>[^/.]+)/unlike\.(?P<format>[a-z0-9]+)/?$ [name='post-unlike']
posts/ ^$ [name='api-root']
posts/ ^\.(?P<format>[a-z0-9]+)/?$ [name='api-root']

'''