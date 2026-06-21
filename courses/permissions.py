from rest_framework import permissions

class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow instructors to create courses.
    Read permissions are allowed to any request,
    so we'll always allow GET, HEAD or OPTIONS requests.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions (POST) are only allowed to authenticated users with the INSTRUCTOR role
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'INSTRUCTOR'
        )

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Update and Delete permissions are only allowed to the instructor who owns the course
        return obj.instructor == request.user
