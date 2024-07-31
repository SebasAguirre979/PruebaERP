from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.

class User(models.Model):
    cedula = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "role"

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = "permission"

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "module"

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        db_table = "rolepermission"

    def __str__(self):
        return f"{self.role.name} - {self.permission.name} - {self.module.name}"

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        db_table = "userrole"

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        db_table = "userpermission"

    def __str__(self):
        return f"{self.user.username} - {self.permission.name} - {self.module.name}"