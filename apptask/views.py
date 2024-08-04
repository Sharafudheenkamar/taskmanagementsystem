from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, filters
from django.core.cache import cache
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from .models import Project,Task
from .serializers import ProjectSerializer,TaskSerializer,UserSerializer
from .pagination import CustomPagination
from .filters import ProjectFilter,TaskFilter,UserFilter
from user.models import Userprofile
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrManagerOrUserUser,IsAdminUser,IsManagerUser,IsUserUser,IsAdminOrManagerUser
from django.db.models import Q
# class AdminView(AdminRequiredMixin, APIView):
#     def get(self, request, *args, **kwargs):
#         # Admin-specific code can go here
#         return Response({"message": "Welcome, Admin!"}, status=status.HTTP_200_OK)
# # your_app/views.py
from .tasks import send_task_notification

def some_view(request):
    # Trigger the task
    send_task_notification.delay('user@example.com', task_id)
    # Rest of your view logic

from django.core.cache import cache

def get_task(task_id):
    task = cache.get(f'task_{task_id}')
    if not task:
        task = Task.objects.get(id=task_id)
        cache.set(f'task_{task_id}', task, 300)  # Cache for 5 minutes
    return task



CACHE_TTL = 60 * 15  # Cache timeout in seconds (15 minutes)
# views.py



class ProjectListCreateView(APIView):
    
    permission_classes = [IsAuthenticated, IsAdminOrManagerUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = ProjectFilter
    ordering_fields = ['name', 'end_date']
    search_fields = ['name', 'end_date']
    
    def get(self, request, *args, **kwargs):
        user = request.user
        print(f"User: {user}")
        print(f"User's Permissions: {user.get_all_permissions()}")

        cache_key = 'projects_all'
        projects = cache.get(cache_key)

        if not projects:
            queryset = Project.objects.all().select_related('created_by').prefetch_related('assigned_to')

            # Apply filters using DjangoFilterBackend
            filterset = ProjectFilter(request.GET, queryset=queryset)
            if not filterset.is_valid():
                return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
            print(filterset)
            queryset = filterset.qs

            # Handle ordering
            ordering = request.GET.get('ordering', None)
            if ordering:
                queryset = queryset.order_by(*ordering.split(','))

            # Handle search
            search = request.GET.get('search', None)
            if search:
                search_filters = Q()
                for field in self.search_fields:
                    search_filters |= Q(**{f"{field}__icontains": search})
                queryset = queryset.filter(search_filters)

            # Ensure queryset is ordered before pagination
            queryset = queryset.order_by(*self.ordering_fields)

            # Pagination
            paginator = CustomPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = ProjectSerializer(page, many=True)

            # Cache the serialized results
            cache.set(cache_key, serializer.data, timeout=CACHE_TTL)
            return paginator.get_paginated_response(serializer.data)
        
        # Deserialize the cached data
        return Response(projects)

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManagerUser]
    def get_object(self, pk):
        return get_object_or_404(Project.objects.select_related('created_by').prefetch_related('assigned_to'), pk=pk)

    def get(self, request, pk, *args, **kwargs):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('projects_all')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        project = self.get_object(pk)
        project.delete()
        cache.delete('projects_all')
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManagerUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = TaskFilter
    ordering_fields = ['field1', 'field2']
    search_fields = ['field1', 'field2']

    def get(self, request, *args, **kwargs):
        cache_key = 'tasks_all'
        tasks = cache.get(cache_key)
        if not tasks:
            queryset = Task.objects.all().select_related('related_field').prefetch_related('another_related_field')
            filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
            filterset = TaskFilter(request.GET, queryset=queryset)
            if not filterset.is_valid():
                return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
            queryset = filterset.qs
            ordering = request.GET.get('ordering', None)
            if ordering:
                queryset = queryset.order_by(*ordering.split(','))
            search = request.GET.get('search', None)
            if search:
                queryset = queryset.filter(*search_fields, search=search)
            paginator = CustomPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = TaskSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('tasks_all')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrManagerUser]
    def get_object(self, pk):
        return get_object_or_404(Task.objects.select_related('related_field').prefetch_related('another_related_field'), pk=pk)

    def get(self, request, pk, *args, **kwargs):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('tasks_all')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        task = self.get_object(pk)
        task.delete()
        cache.delete('tasks_all')
        return Response(status=status.HTTP_204_NO_CONTENT)
class UserListCreateView(APIView):
    permission_classes=[IsAuthenticated,IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = UserFilter
    ordering_fields = ['field1', 'field2']
    search_fields = ['field1', 'field2']

    def get(self, request, *args, **kwargs):
        cache_key = 'users_all'
        users = cache.get(cache_key)
        if not users:
            queryset = Userprofile.objects.all().select_related('related_field').prefetch_related('another_related_field')
            filterset = UserFilter(request.GET, queryset=queryset)
            if not filterset.is_valid():
                return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
            queryset = filterset.qs
            ordering = request.GET.get('ordering', None)
            if ordering:
                queryset = queryset.order_by(*ordering.split(','))
            search = request.GET.get('search', None)
            if search:
                queryset = queryset.filter(*search_fields, search=search)
            paginator = CustomPagination()
            page = paginator.paginate_queryset(queryset, request)
            serializer = UserSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('users_all')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_object(self, pk):
        return get_object_or_404(Userprofile.objects.select_related('related_field').prefetch_related('another_related_field'), pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Invalidate the cache after updating a user
            cache.delete('users_all')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        # Invalidate the cache after deleting a user
        cache.delete('users_all')
        return Response(status=status.HTTP_204_NO_CONTENT)



