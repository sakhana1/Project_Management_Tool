from rest_framework.permissions import BasePermission, SAFE_METHODS

class ProjectAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or obj.members.filter(id=request.user.id).exists()
