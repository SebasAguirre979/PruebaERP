from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from seguridad.views import UserViewSet, RoleViewSet, PermissionViewSet, ModuleViewSet, RolePermissionViewSet, UserRoleViewSet, UserPermissionViewSet

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
    path('', include(router.urls))
]
