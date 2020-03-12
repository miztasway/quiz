from django.contrib import admin

# Register your models here.

from .models import Quiz, Answer, Question, Solution, Choice

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(Answer)
admin.site.register(Choice)