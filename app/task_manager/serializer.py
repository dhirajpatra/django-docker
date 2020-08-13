from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from task_manager.models import Task, Comment


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user creation
    """
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(required=True, min_length=8)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'password')


class UserLoginSerializer(serializers.ModelSerializer):
    """"
    Serializer for user login
    """
    username = serializers.CharField(label='Username', write_only=True, required=True)
    password = serializers.CharField(label='Password', write_only=True, min_length=8, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer for task managing
    """

    class Meta:
        model = Comment
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    """
    serializer for task managing
    """
    task_comment = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'modified_at', 'task_comment']