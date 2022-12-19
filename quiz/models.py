from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lesson(models.Model): 
    text = models.CharField(max_length=100)

    def __str__(self): 
        return f"{self.id}__{self.text}"

class Question(models.Model): 
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    text=models.CharField(max_length=300)

    def __str__(self): 
        return f"lesson_id:{self.lesson.id}__id:{self.id}__{self.text}"


class Choices (models.Model): 
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    is_true = models.BooleanField(default=False)

    def __str__(self): 
        return f"question_id:{self.question.id}__id:{self.id}__{self.text}__{self.is_true}"

class QuizInstance(models.Model): 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)
    score = models.FloatField()

    def __str__(self): 
        return f"instance_id : {self.id}_user:{self.user.id}_lesson:{self.lesson.id}_score:{self.score}_created={self.created}"


