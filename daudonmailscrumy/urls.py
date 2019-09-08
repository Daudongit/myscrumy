from django.conf.urls import include, url
from rest_framework import routers
# from rest_framework.authtoken import views as auth_views
from . import views

app_name = "daudonmailscrumy"

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'scrumuser', views.ScrumUserViewSet)
router.register(r'scrumgoal', views.ScrumGoalViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'api-token-auth', views.CustomAuthToken.as_view(), name='api-token-auth')
    # url(r'api-token-auth', auth_views.obtain_auth_token, name='api-token-auth')
]