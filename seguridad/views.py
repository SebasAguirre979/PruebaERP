from rest_framework import viewsets, status
from .models import User, Role, Permission, Module, RolePermission, UserRole, UserPermission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer, ModuleSerializer, RolePermissionSerializer, UserRoleSerializer, UserPermissionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.db import transaction

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

class CreateUserView(APIView):
    def post(self, request):
        cedula = request.data.get('cedula')
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(cedula=cedula).exists():
            return Response({'error': 'El usuario ya está creado.'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'El nombre de usuario ya está en uso.'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'El correo electrónico ya está en uso.'}, status=400)
        
        User.objects.get_or_create(cedula=cedula, username=username, email=email, password=password)
        
        return Response({
            'message': 'Usuario creado'
        }, status=201)
    
class UserChangePassword(APIView):
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
            return Response({'error':'El usuario no existe'}, status=404)
        
        user_role = UserRole.objects.filter(user=user)
        user_permission = UserPermission.objects.filter(user=user)
        permissions_data = []
        
        user_date = {
            'usuario': user.username,
            'roles': [rol.role.name for rol in user_role],
            'permisos_especiales': permissions_data
        }

        for permission in user_permission:
            type_data = {
                'modulo': permission.module.name,
                'permiso': permission.permission.name
            }
            permissions_data.append(type_data)

        return Response(user_date, status=200)
    
class CreateRoleWithPermission(APIView):
    @transaction.atomic
    def post(self, request):
        role_name = request.data.get('role_name')
        permissions_data = request.data.get('permissions', [])

        if Role.objects.filter(name=role_name).exists():
            return Response({'error': 'Ya existe un rol con este nombre.'}, status=400)

        try:
            role = Role.objects.create(name=role_name)

            for permission_entry in permissions_data:
                module_id = permission_entry.get('module_id')
                permission_ids = permission_entry.get('permission_ids', [])

                try:
                    module = Module.objects.get(id=module_id)
                except Module.DoesNotExist:
                    raise ValueError(f'Módulo con id {module_id} no encontrado.')

                for permission_id in permission_ids:
                    try:
                        permission = Permission.objects.get(id=permission_id)
                    except Permission.DoesNotExist:
                        raise ValueError(f'Permiso con id {permission_id} no encontrado.')

                    RolePermission.objects.get_or_create(role=role, permission=permission, module=module)

        except ValueError as e:
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=400)

        return Response({
            'message': 'Rol creado y permisos asignados exitosamente.',
            'rol_id': role.id,
            'rol_nombre': role.name
        }, status=201)
    
class AddRolesAndPermissionsUser(APIView):
    @transaction.atomic
    def post(self, request):
        user_id = request.data.get('user_id')
        role_ids = request.data.get('role_ids', [])
        permissions_data = request.data.get('permissions', [])

        try:
            user = User.objects.get(cedula=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=404)

        roles = Role.objects.filter(id__in=role_ids)
        if len(roles) != len(role_ids):
            return Response({'error': 'Uno o más roles no existen.'}, status=404)
        
        try:
            for role in roles:
                UserRole.objects.get_or_create(user=user, role=role)

            for permission_entrante in permissions_data:
                module_id = permission_entrante.get('module_id')
                permission_ids = permission_entrante.get('permission_ids', [])

                try:
                    module = Module.objects.get(id=module_id)
                except Module.DoesNotExist:
                    return Response({'error': f'Módulo con id {module_id} no encontrado.'}, status=404)

                for permission_id in permission_ids:
                    try:
                        permission = Permission.objects.get(id=permission_id)
                    except Permission.DoesNotExist:
                        return Response({'error': f'Permiso con id {permission_id} no encontrado.'}, status=404)

                    UserPermission.objects.get_or_create(user=user, permission=permission, module=module)
                    
        except ValueError as e:
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=400)

        return Response({
            'message': 'Roles y permisos asignados exitosamente.',
            'cedula': user.cedula
        }, status=200)
    
class VerifyUser(APIView):
    def post(self, request):
        cedula = request.data.get('cedula')
        password = request.data.get('password')

        try:
            user = User.objects.get(cedula=cedula)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado.'}, status=404)

        if not check_password(password, user.password):
            return Response({'error': 'Contraseña incorrecta.'}, status=404)

        roles = Role.objects.filter(userrole__user=user)

        user_permissions = UserPermission.objects.filter(user=user)
        permissions_data = []
        
        for perm in user_permissions:
            type_data = {
                'module': perm.module.name,
                'permission': perm.permission.name
            }
            permissions_data.append(type_data)

        response_data = {
            'cedula': user.cedula,
            'usuario': user.username,
            'roles': [role.name for role in roles],
            'permisos_especiales': permissions_data
        }

        return Response(response_data, status=200)