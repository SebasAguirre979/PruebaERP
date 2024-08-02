from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from seguridad.views import *

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
    path('create-user-and-assign-role/', CreateUserView.as_view(), name='create-user-and-assign-role'),
    path('change-password/<int:cedula>', UserChangePassword.as_view(), name='change-password'),
    path('role-permission/<int:cedula>', UserPermissionRole.as_view(), name='role-permission'),
    path('create-role-with-permission/', CreateRoleWithPermission.as_view(), name='create-role-with-permission'),
    path('add-roles-and-permissions-user/', AddRolesAndPermissionsUser.as_view(), name='add-roles-and-permissions-user'),
    path('verify-user/', VerifyUser.as_view(), name='verify-user'),
]
