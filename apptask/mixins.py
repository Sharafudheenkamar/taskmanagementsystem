from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUser,IsManagerUser,IsUserUser

class AdminRequiredMixin:
    permission_classes = [IsAuthenticated, IsAdminUser]
class ManagerRequiredMixin:
    permission_classes = [IsAuthenticated, IsManagerUser]
class UserRequiredMixin:
    permission_classes = [IsAuthenticated, IsUserUser]

