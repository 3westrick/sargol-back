from rest_framework import permissions
from django.contrib.auth.models import User
class IsStaffEditorPermission(permissions.DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # def has_permission(self, request, view):
        
    #     if not request.user.is_staff:
    #         return False
    #     return super().has_permission(request, view)

    # def has_permission(self, request, view):
    #     user = request.user
    #     pers = user.get_all_permissions()
    #     print(1,user)
    #     if user.is_staff:
    #         if user.has_perm("attribute.view_attribute"): # change_attribute | add_attribute | delete_attribute
    #             return True
    #         return False
    #     return False
    
    def has_object_permission(self, request, view, obj):
        return False