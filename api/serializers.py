from rest_framework import serializers
from .models import (User, Education, Experience, ProfileSkills, UserProject,
                     PriceAvailablity, DeveloperProfile, Notification)
from django.contrib.auth.hashers import make_password


# user serializer class
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # function to validate and save passwords
    def validate_password(self, value: str) -> str:
        """
        A method to validate and save passwords in simple text format
        """
        return make_password(value)


class DeveloperProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = DeveloperProfile
        fields = '__all__'


class DeveloperProfileSerializerRead(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DeveloperProfile
        fields = '__all__'
        depth = 2


class EducationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = Education
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = Experience
        fields = '__all__'


class ProfileSkillsSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = ProfileSkills
        fields = '__all__'


class UserProjectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = UserProject
        fields = '__all__'


class PriceAvailablitySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = PriceAvailablity
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = Notification
        fields = '__all__'
