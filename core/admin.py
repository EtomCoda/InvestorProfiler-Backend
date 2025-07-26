from django.contrib import admin
from .models import Question, Option, RiskProfile, ProfileMapping 

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'text', 'category')
    inlines = [OptionInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(RiskProfile)
admin.site.register(ProfileMapping)
