from rest_framework.routers import DefaultRouter
from .views import (
    CommentViewSet,
    ContributorViewSet,
    IssueViewSet,
    ProjectViewSet,
)

router = DefaultRouter()

router.register("projects", ProjectViewSet, basename="project")
router.register("contributors", ContributorViewSet, basename="contributor")
router.register("issues", IssueViewSet, basename="issue")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = router.urls