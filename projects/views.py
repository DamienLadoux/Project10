from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Project, Contributor, Issue, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    ProjectSerializer,
)

# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        return Project.objects.filter(
            contributors__user=user
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(
            project=project,
            user=self.request.user,
        )

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user

        return Contributor.objects.filter(
            project__contributors__user=user
        )

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]

        if not Contributor.objects.filter(
            project=project,
            user=self.request.user,
        ).exists():
            raise PermissionDenied(
                "Vous devez être contributeur du projet."
            )

        serializer.save()


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        return Issue.objects.filter(
            project__contributors__user=user
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.validated_data["project"]
        assignee = serializer.validated_data["assignee"]

        is_contributor = Contributor.objects.filter(
            project=project,
            user=self.request.user,
        ).exists()

        if not is_contributor:
            raise PermissionDenied(
                "Vous devez être contributeur du projet."
            )

        assignee_is_contributor = Contributor.objects.filter(
            project=project,
            user=assignee,
        ).exists()

        if not assignee_is_contributor:
            raise serializers.ValidationError(
                {
                    "assignee": (
                        "L'utilisateur assigné doit être "
                        "contributeur du projet."
                    )
                }
            )

        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,IsAuthorOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        return Comment.objects.filter(
            issue__project__contributors__user=user
        ).distinct()

    def perform_create(self, serializer):
        issue = serializer.validated_data["issue"]

        is_contributor = Contributor.objects.filter(
            project=issue.project,
            user=self.request.user,
        ).exists()

        if not is_contributor:
            raise PermissionDenied(
                "Vous devez être contributeur du projet."
            )

        serializer.save(author=self.request.user)