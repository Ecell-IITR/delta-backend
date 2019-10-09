from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    '''
    Check if user is student or not
    '''

    def has_object_permission(self, request, view, obj):
        return request.user.is_student
