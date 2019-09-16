from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

AuthUser = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=50)
    user = models.ManyToManyField(AuthUser, blank=True)

class GoalStatus(models.Model):
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name

class ScrumyGoals(models.Model):
    goal_name = models.CharField(max_length=50)
    goal_id = models.IntegerField()
    created_by = models.CharField(max_length=50)
    moved_by = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    user = models.ForeignKey(AuthUser, related_name='ScrumyGoals', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.goal_name

    def get_absolute_url(self):
        return reverse('daudonmailscrumy:movegoal', kwargs={
            'goal_id': self.goal_id
        })


class ScrumyHistory(models.Model):
    moved_by = models.CharField(max_length=50)
    created_by = models.CharField(max_length=50)
    moved_from = models.CharField(max_length=50)
    moved_to = models.CharField(max_length=50)
    time_of_action = models.DateTimeField(auto_now_add=True)
    goal = models.ForeignKey(ScrumyGoals, on_delete=models.CASCADE)

    def __str__(self):
        return self.moved_by

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    