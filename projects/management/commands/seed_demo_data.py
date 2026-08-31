from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import Comment, Contributor, Issue, Project
from users.models import User


DEMO_PASSWORD = "DemoPass123!"


class Command(BaseCommand):
    help = "Crée des données de démonstration pour tester l'API avec Postman."

    def create_user(self, username, first_name, last_name, email):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "age": 30,
                "can_be_contacted": True,
                "can_data_be_shared": False,
            },
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
        return user

    @transaction.atomic
    def handle(self, *args, **options):
        alice = self.create_user(
            "alice", "Alice", "Martin", "alice@example.com"
        )
        bob = self.create_user("bob", "Bob", "Durand", "bob@example.com")
        clara = self.create_user(
            "clara", "Clara", "Bernard", "clara@example.com"
        )
        david = self.create_user(
            "david", "David", "Petit", "david@example.com"
        )

        softdesk, _ = Project.objects.get_or_create(
            title="Application SoftDesk",
            defaults={
                "description": "API de suivi des projets et de leurs tickets.",
                "type": "back-end",
                "author": alice,
            },
        )
        mobile, _ = Project.objects.get_or_create(
            title="Application mobile",
            defaults={
                "description": "App mobile destinée aux équipes terrain",
                "type": "mobile",
                "author": bob,
            },
        )

        contributors = [
            (alice, softdesk, "author", "Responsable produit"),
            (bob, softdesk, "contributor", "Développeur back-end"),
            (clara, softdesk, "contributor", "Développeuse front-end"),
            (bob, mobile, "author", "Responsable produit"),
            (clara, mobile, "contributor", "Développeuse mobile"),
            (david, mobile, "contributor", "Testeur"),
        ]
        for user, project, permission, role in contributors:
            Contributor.objects.get_or_create(
                user=user,
                project=project,
                defaults={"permission": permission, "role": role},
            )

        issue_1, _ = Issue.objects.get_or_create(
            title="Corriger l'authentification JWT",
            project=softdesk,
            defaults={
                "description": "Le jeton doit être refusé après expiration.",
                "tag": "bug",
                "priority": "high",
                "status": "in-progress",
                "author": alice,
                "assignee": bob,
            },
        )
        Issue.objects.get_or_create(
            title="Documenter les endpoints",
            project=softdesk,
            defaults={
                "description": "Ajouter des exemples de requêtes Postman.",
                "tag": "task",
                "priority": "medium",
                "status": "to-do",
                "author": clara,
                "assignee": clara,
            },
        )
        Issue.objects.get_or_create(
            title="Améliorer le mode hors ligne",
            project=mobile,
            defaults={
                "description": "Prévoir synchronisation après reconnexion.",
                "tag": "improvement",
                "priority": "low",
                "status": "to-do",
                "author": bob,
                "assignee": david,
            },
        )
        Comment.objects.get_or_create(
            issue=issue_1,
            author=bob,
            description="Le scénario d'expiration est reproduit et en correction.",
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Données de démonstration prêtes. "
                "Comptes : alice, bob, clara, david "
                f"(mot de passe : {DEMO_PASSWORD})."
            )
        )
