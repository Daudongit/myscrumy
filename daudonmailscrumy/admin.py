from django.contrib import admin
from .models import GoalStatus, ScrumyGoals, ScrumyHistory, Project

class GoalStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name')

class ScrumyGoalsAdmin(admin.ModelAdmin):
    list_display = ('id', 'goal_name', 'goal_status')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by')

admin.site.register(GoalStatus, GoalStatusAdmin)
admin.site.register(ScrumyGoals, ScrumyGoalsAdmin)
admin.site.register(ScrumyHistory)
admin.site.register(Project, ProjectAdmin)
