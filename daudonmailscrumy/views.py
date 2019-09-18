
import random
# from rest_framework.decorators import action
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from account.models import Company, ScrumUser

from .csrf_exempt import CsrfExemptSessionAuthentication
from .models import GoalStatus, Project, ScrumyGoals, User
from .serializers import (
    ScrumGoalSerializer, ScrumUserSerializer,
    UserSerializer, ProjectSerializer
)

# from rest_framework import permissions

class ScrumUserViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    permission_classes = []

    def create(self, request):
        print(request)
        request.data['company_id'] = 1
        serializer = ScrumUserSerializer(
            data=request.data, context={'request':request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def retrieve(self, request, pk=None):
        # print(request.query_params.get('project'))
        queryset = ScrumUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ScrumUserSerializer(user, context={'request':request})
        return Response(serializer.data)

    # @action(methods=['post'], detail=False)
    # def myscrum(self, request, *args, **kwargs):
    #     # users = 
    #     return Response(
    #         {'success': 'sucessfully tested'},
    #         status=status.HTTP_202_ACCEPTED
    #     )


class ScrumGoalViewSet(viewsets.ModelViewSet):
    queryset = ScrumyGoals.objects.all()
    serializer_class = ScrumGoalSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     # return ScrumyGoals.objects.filter(project=self.request.project)
    #     return ScrumyGoals.objects.filter(project=2)

    def create(self, request):
        goal_creator = request.user
        request_data = {'goal_name':request.data['goal_name']}
        request_data['goal_id'] = generate_goal_id()
        request_data['created_by'] = goal_creator.username
        request_data['moved_by'] = goal_creator.username
        request_data['owner'] = goal_creator.username
        # request_data['goal_status'] = GoalStatus.objects.get(status_name="Weekly Goal")
        request_data['user'] = goal_creator.id
        request_data['project'] = request.data['project_id']
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
                'id':user.id,   
                'username':user.username,   
                'user_type':user.user_type,
                'company':{'name':Company.objects.get(pk=user.company_id).name},
                'project':Project.objects.get(title=request.data['project']).id
            }
        })

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

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
