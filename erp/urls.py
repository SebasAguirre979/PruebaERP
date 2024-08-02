from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from seguridad.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-user/', CreateUserView.as_view(), name='create-user'),
    path('change-password/<int:cedula>', UserChangePassword.as_view(), name='change-password'),
    path('role-permission/<int:cedula>', UserPermissionRole.as_view(), name='role-permission'),
    path('create-role-with-permission/', CreateRoleWithPermission.as_view(), name='create-role-with-permission'),
    path('add-roles-and-permissions-user/', AddRolesAndPermissionsUser.as_view(), name='add-roles-and-permissions-user'),
    path('verify-user/', VerifyUser.as_view(), name='verify-user'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
