
import random
from django.contrib.auth import authenticate, get_user_model, login
# from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication 
from account.models import ScrumUser
from .csrf_exempt import CsrfExemptSessionAuthentication
from .models import ScrumyGoals, GoalStatus
from .serializers import (ScrumGoalSerializer, ScrumUserSerializer,
                          UserSerializer)

# from rest_framework import permissions


User = get_user_model()

class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    permission_classes = []

    def create(self, request):
        serializer = ScrumUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        # return Response({'created': False})


class ScrumGoalViewSet(viewsets.ModelViewSet):
    queryset = ScrumyGoals.objects.all()
    serializer_class = ScrumGoalSerializer

    def create(self, request):
        goal_creator = request.user
        request_data = {'goal_name':request.data['goal_name']}
        request_data['goal_id'] = generate_goal_id()
        request_data['created_by'] = goal_creator.username
        request_data['moved_by'] = goal_creator.username
        request_data['owner'] = goal_creator.username
        # request_data['goal_status'] = GoalStatus.objects.get(status_name="Weekly Goal")
        request_data['user'] = goal_creator.id
        serializer = ScrumGoalSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)  

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    
    def create(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = self.serializer_class(user)
            return Response({'success': 'ok'}, status=status.HTTP_200_OK)
            # return Response(serializer.data, status=status.HTTP_200_OK)
        raise AuthenticationFailed



#goal_id generator helper
def generate_goal_id():
    goal_id = 0
    while True:
        random_number = random.randint(1000,9999)
        scrumy_goals = ScrumyGoals.objects.filter(goal_id = random_number)
        if not len(scrumy_goals):
            goal_id = random_number
            break
    return goal_id