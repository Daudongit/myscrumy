
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from . import views

app_name = "daudonmailscrumy"

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'scrumuser', views.ScrumUserViewSet)
router.register(r'scrumgoal', views.ScrumGoalViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]