from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, TeamView, ActivityView, dashboard

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
    path("dashboard/", dashboard, name="dashboard"),
    path("team/", TeamView.as_view(), name="team"),
    path("activity/", ActivityView.as_view(), name="activity"),
]
