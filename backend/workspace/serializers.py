from django.contrib.auth import get_user_model
from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone
from .models import Project, Task, Activity

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name")
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # Starter content makes every workspace useful immediately; all records
        # are owned by the new account and remain isolated from other users.
        today = timezone.localdate()
        project_a = Project.objects.create(
            name="Website refresh",
            description="A focused redesign to make the product experience clearer and faster.",
            status="active", owner=user, due_date=today + timedelta(days=14),
        )
        project_b = Project.objects.create(
            name="Launch planning",
            description="Coordinate launch messaging, assets, and the final checklist.",
            status="planning", owner=user, due_date=today + timedelta(days=21),
        )
        project_a.members.add(user)
        project_b.members.add(user)
        starter_tasks = [
            (project_a, "Review the current experience", "Collect the key friction points from the current site.", "completed", "medium", 0),
            (project_a, "Create the page structure", "Map the main pages and navigation hierarchy.", "in_progress", "high", 2),
            (project_a, "Prepare the visual direction", "Define typography, spacing, and reusable components.", "todo", "medium", 5),
            (project_b, "Draft the launch checklist", "List owners, deliverables, and target dates.", "in_progress", "high", 3),
            (project_b, "Prepare launch content", "Outline the announcement and supporting content.", "todo", "low", 8),
        ]
        for project, title, description, status, priority, offset in starter_tasks:
            Task.objects.create(
                project=project, created_by=user, assignee=user, title=title,
                description=description, status=status, priority=priority,
                due_date=today + timedelta(days=offset),
            )
        Activity.objects.create(user=user, message='Created your Planora starter workspace')
        return user

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "full_name")
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username

class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)
    task_count = serializers.IntegerField(read_only=True)
    completed_count = serializers.IntegerField(read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(source="members", many=True, queryset=User.objects.all(), required=False, write_only=True)
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ("id", "name", "description", "status", "color", "owner", "owner_name", "members", "member_ids", "due_date", "task_count", "completed_count", "created_at", "updated_at")
        read_only_fields = ("owner", "created_at", "updated_at")

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    assignee_name = serializers.CharField(source="assignee.username", read_only=True, default=None)
    class Meta:
        model = Task
        fields = ("id", "title", "description", "project", "project_name", "created_by", "assignee", "assignee_name", "status", "priority", "due_date", "created_at", "updated_at")
        read_only_fields = ("created_by", "created_at", "updated_at")

    def validate_project(self, project):
        request = self.context.get("request")
        if request and not (project.owner_id == request.user.id or project.members.filter(id=request.user.id).exists()):
            raise serializers.ValidationError("You can only add tasks to projects in your workspace.")
        return project

class ActivitySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    class Meta:
        model = Activity
        fields = ("id", "username", "message", "created_at")
