from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Instructor").exists()


class IsBookkeeper(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Bookkeeper").exists()


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Manager").exists()
