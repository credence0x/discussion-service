from rest_framework import serializers
from .models import Post

class PostsSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    likes = serializers.IntegerField(read_only=True)
    users_who_liked = serializers.StringRelatedField(many=True,read_only=True)
    
    class Meta:
        model = Post
        fields = ('id','creator','content','likes','users_who_liked','date_created')
        
