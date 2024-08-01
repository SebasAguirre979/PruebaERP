from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from seguridad.views import UserViewSet, RoleViewSet, PermissionViewSet, ModuleViewSet, RolePermissionViewSet, UserRoleViewSet, UserPermissionViewSet, CreateUserAndAssignRoleView, UserChangePasswordView, UserPermissionRole

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'modules', ModuleViewSet)
router.register(r'role-permissions', RolePermissionViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'user-permissions', UserPermissionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('create-user-and-assign-role/', CreateUserAndAssignRoleView.as_view(), name='create-user-and-assign-role'),
    path('change-password/<int:cedula>', UserChangePasswordView.as_view(), name='change-password'),
    path('role-permission/<int:cedula>', UserPermissionRole.as_view(), name='role-permission'),
]
