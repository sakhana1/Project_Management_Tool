from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Project, Task, Activity
from .serializers import RegisterSerializer, UserSerializer, ProjectSerializer, TaskSerializer, ActivitySerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Project.objects.filter(Q(owner=self.request.user) | Q(members=self.request.user)).distinct().annotate(
            task_count=Count("tasks", distinct=True),
            completed_count=Count("tasks", filter=Q(tasks__status="completed"), distinct=True),
        ).order_by("-updated_at")
    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        project.members.add(self.request.user)
        Activity.objects.create(user=self.request.user, message=f'Created project "{project.name}"')
    def perform_update(self, serializer):
        project = serializer.save()
        Activity.objects.create(user=self.request.user, message=f'Updated project "{project.name}"')
    def perform_destroy(self, instance):
        Activity.objects.create(user=self.request.user, message=f'Deleted project "{instance.name}"')
        instance.delete()

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Task.objects.filter(Q(project__owner=self.request.user) | Q(project__members=self.request.user)).distinct().order_by("due_date", "-updated_at")
    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)
        Activity.objects.create(user=self.request.user, message=f'Created task "{task.title}"')
    def perform_update(self, serializer):
        task = serializer.save()
        Activity.objects.create(user=self.request.user, message=f'Updated task "{task.title}"')
    def perform_destroy(self, instance):
        Activity.objects.create(user=self.request.user, message=f'Deleted task "{instance.title}"')
        instance.delete()

class TeamView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(Q(owned_projects__owner=self.request.user) | Q(shared_projects__owner=self.request.user)).distinct().order_by("username")

class ActivityView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by("-created_at")[:30]

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    projects = Project.objects.filter(Q(owner=request.user) | Q(members=request.user)).distinct()
    tasks = Task.objects.filter(project__in=projects)
    total = tasks.count()
    completed = tasks.filter(status="completed").count()
    overdue = tasks.filter(due_date__lt=timezone.localdate()).exclude(status="completed").count()
    return Response({
        "project_count": projects.count(),
        "task_count": total,
        "completed_count": completed,
        "pending_count": tasks.exclude(status="completed").count(),
        "overdue_count": overdue,
        "completion_rate": round((completed / total) * 100) if total else 0,
        "recent_tasks": TaskSerializer(tasks.order_by("-updated_at")[:5], many=True).data,
    })
