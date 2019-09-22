# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ScrumyGoals, GoalStatus, User, Project
from  account.models import ScrumUser, Company

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
       

class GoalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalStatus
        fields = '__all__'

class ScrumGoalSerializer(serializers.ModelSerializer):
    goal_status = GoalStatusSerializer(many=False, read_only=True)
    
    def create(self, validated_data):
        return ScrumyGoals.objects.create(
            goal_status=GoalStatus.objects.get(status_name="Weekly Goal"),
            **validated_data
        )
    
    # def update(self, instance, validated_data):
    #     # goal_status = validated_data.pop('goal_status')
    #     # instance.goal_status_id = goal_status.id
    #     return instance

    class Meta:
        model = ScrumyGoals
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'write_only': True},
            'moved_by': {'write_only': True},
            'owner': {'write_only': True},
            'user': {'write_only': True},
            'project': {'write_only': True}
        }

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')

class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        project_id = self.context['request'].query_params.get('project')
        data = data.filter(project_id=project_id)
        return super(FilteredListSerializer, self).to_representation(data)


class ScrumGoalFilterSerializer(serializers.ModelSerializer):
    goal_status = GoalStatusSerializer(many=False, read_only=True)

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = ScrumyGoals
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'write_only': True},
            'moved_by': {'write_only': True},
            'owner': {'write_only': True},
            'user': {'write_only': True},
            'project': {'write_only': True}
        }

class ScrumUserSerializer(serializers.ModelSerializer):
    ScrumyGoals = ScrumGoalFilterSerializer(many=True, read_only=True)
    # company = CompanySerializer(many=False, read_only=True)
    # company_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Company.objects.all(), source='company', write_only=True
    # )
    
    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data.pop('password')
        return ScrumUser.objects.create(
            password=make_password(password),
            **validated_data
        )

    class Meta:
        model = ScrumUser
        fields = (
            'id', 'username', 
            'full_name', 'user_type', 
            'password', 'ScrumyGoals'
            # 'company','company_id'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'user')
        extra_kwargs = {
            'user': {'write_only': True}
        }