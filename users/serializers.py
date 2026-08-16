from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'age',
            'can_be_contacted',
            'can_data_be_shared'
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def validate_age(self, value):
        if value < 15:
            raise serializers.ValidationError(
                "L'utilisateur doit avoir au moins 15ans"
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance