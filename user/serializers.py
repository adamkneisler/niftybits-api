from rest_framework import serializers

from django.contrib.auth.models import User
from .models import NiftyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username')
        user = User(username=username)
        user.set_password(password)
        user.save()
        n_user = NiftyUser.objects.create(
            user=user,
            profile_name=username,
            handle=username
        )
        return user