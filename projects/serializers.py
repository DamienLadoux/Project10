from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "type",
            "created_time",
            "author",
        ]

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            "id",
            "user",
            "project",
            "permission",
            "role",
        ]

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            "id",
            "title",
            "description",
            "tag",
            "priority",
            "status",
            "created_time",
            "author",
            "assignee",
            "project",
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "description",
            "created_time",
            "author",
            "issue",
        ]