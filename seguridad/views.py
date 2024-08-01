from rest_framework import viewsets, status
from .models import User, Role, Permission, Module, RolePermission, UserRole, UserPermission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, ModuleSerializer, RolePermissionSerializer, UserRoleSerializer, UserPermissionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer

class UserPermissionViewSet(viewsets.ModelViewSet):
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer

class CreateUserAndAssignRoleView(APIView):
    def post(self, request):
        cedula = request.data.get('cedula')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(cedula=cedula).exists():
            return Response({'error': 'El usuario ya está creado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'El nombre de usuario ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User(cedula=cedula, username=username, email=email, password=password)
        user.save()

        return Response({
            'message': 'Usuario creado'
        }, status=201)
    
class UserChangePasswordView(APIView):
    def post(self, request, cedula):
        password_antigua = request.data.get('password_antigua')
        password_nueva = request.data.get('password_nueva')

        if not password_nueva:
            return Response({'error': 'La contraseña nueva no puede estar vacía'}, status=400)
        
        try:
            user = User.objects.get(cedula=cedula)
        except User.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=400)

        password_coincide = check_password(password_antigua, user.password)
        if not password_coincide:
            return Response({'error': 'La contraseña antigua es incorrecta'}, status=400)

        user.password = password_nueva
        user.save()

        return Response({
            'message': 'Contraseña cambiada exitosamente'
            }, status=201)
    
class UserPermissionRole(APIView):
    def get(self, request, cedula, format=None):
        try:
            user = User.objects.get(cedula=cedula)
        except User.DoesNotExist:
            return Response({'error':'el usuario no existe'}, status=404)
        
        user_role = UserRole.objects.filter(user=user)
        user_permission = UserPermission.objects.filter(user=user)

        roles_data = []
        permissions_data = []
        
        user_date = {
            'usuario': user.username,
            'roles': roles_data,
            'permisos_especiales': permissions_data
        }

        for rol in user_role:
            role_data = {
                'rol': rol.role.name

            }
            roles_data.append(role_data)

        for permission in user_permission:
            type_data = {
                'modulo': permission.module.name,
                'permiso': permission.permission.name
            }
            permissions_data.append(type_data)

        return Response(user_date, status=200)