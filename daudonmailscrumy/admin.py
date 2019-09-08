from django.contrib import admin
from .models import GoalStatus, ScrumyGoals, ScrumyHistory

class GoalStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name')

class ScrumyGoalsAdmin(admin.ModelAdmin):
    list_display = ('id', 'goal_name', 'goal_status')

admin.site.register(GoalStatus, GoalStatusAdmin)
admin.site.register(ScrumyGoals, ScrumyGoalsAdmin)
admin.site.register(ScrumyHistory)
