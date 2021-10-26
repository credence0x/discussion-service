from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission): 
    # allows only owners to write except for "PATCH" methods where all users can like a post  
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user

