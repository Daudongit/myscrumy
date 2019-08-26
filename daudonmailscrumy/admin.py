from django.contrib import admin
from .models import GoalStatus, ScrumyGoals, ScrumyHistory


admin.site.register(GoalStatus)
admin.site.register(ScrumyGoals)
admin.site.register(ScrumyHistory)
