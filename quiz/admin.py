from django.contrib import admin
from .models import Lesson, Question, QuizInstance, Choices

# Register your models here.
admin.site.register(Lesson)
admin.site.register(Question)
admin.site.register(QuizInstance)
admin.site.register(Choices)

