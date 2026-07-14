from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(name="ADMIN").exists()


class IsLibrarianOrAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(
            name__in=["ADMIN", "LIBRARIAN"]
        ).exists()