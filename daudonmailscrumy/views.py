
import random

from django.contrib.auth import authenticate, get_user_model, login
# from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import action
from rest_framework.response import Response

from account.models import ScrumUser, Company

from .csrf_exempt import CsrfExemptSessionAuthentication
from .models import GoalStatus, ScrumyGoals, User
from .serializers import (ScrumGoalSerializer, ScrumUserSerializer,
                          UserSerializer)

# from rest_framework import permissions

class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    permission_classes = []

    def create(self, request):
        request.data['company_id'] = 1
        serializer = ScrumUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
        # return Response({'created': False})


class ScrumGoalViewSet(viewsets.ModelViewSet):
    queryset = ScrumyGoals.objects.all()
    serializer_class = ScrumGoalSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    

    def update(self, request, pk=None):
        instance = self.get_object()
        if request.data['mode'] == 'changeowner':
            instance.user = ScrumUser.objects.get(pk=request.data['user_id'])
            instance.goal_status = GoalStatus.objects.get(
                status_name=request.data['status_name']
            )
            # instance.goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
        if request.data['mode'] == 'editgoal':
            instance.goal_name = request.data['goal_name']
        instance.save()
        return Response(
            {'success': 'owner updated', 'goal_id':instance.goal_id}, 
            status=status.HTTP_202_ACCEPTED
        )

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        goal_status = GoalStatus.objects.get(
            status_name=request.data['status_name']
        )
        instance.goal_status = goal_status
        instance.save()
        
        # # request_data = {'goal_status':goal_status}
        # serializer = self.serializer_class(instance, data=request.data, partial=True)
        # serializer.is_valid(raise_exception=True)
        # # serializer.goal_status_id = goal_status.id
        # # serializer.save()
        # serializer.update(instance, validated_data={'goal_status_id':goal_status.id})
        # new_instance = serializer.save()
        # return Response(serializer.data)
        return Response({'success': 'status updated'}, status=status.HTTP_202_ACCEPTED)


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
            serializer = ScrumUserSerializer(user)
            data = serializer.data
            data.pop('ScrumyGoals')
            return Response(
                {'success': 'ok', 'user':data, 'token':''}, 
                status=status.HTTP_200_OK
            )
        raise AuthenticationFailed


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'success':'ok',
            'token': token.key,
            'user': {
                'username':user.username,   
                'user_type':user.user_type,
                'company':{'name':Company.objects.get(pk=user.company_id).name}
            }
        })

#goal_id generator helper
def generate_goal_id():
    goal_id = 0
    while True:
        random_number = random.randint(1000, 9999)
        scrumy_goals = ScrumyGoals.objects.filter(goal_id=random_number)
        if not len(scrumy_goals):
            goal_id = random_number
            break
    return goal_id
