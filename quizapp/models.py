from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.shortcuts import reverse

# Create your models here.

User = get_user_model()

class Quiz(models.Model):
    title = models.CharField(max_length=300)
    user = models.ForeignKey(User, related_name="created_quiz", on_delete=models.CASCADE)
    score_for_each_question = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pass_mark = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    slug = models.SlugField(blank=True)
    time_for_each_question = models.DurationField()
    date  = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return self.title

    
    def __repr__(self):
        return f'<Quiz: {self.title[:30]}>'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug  = slugify(self.title)
        super(Quiz, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("quiz:quiz", slug=self.slug)

    def to_json(self):
        return {
            "title": self.title,
            "score_for_each_question": float(self.score_for_each_question),
            "slug": self.slug,
            "time_for_each_question": str(self.time_for_each_question),
            "pass_mark": float(self.pass_mark),
           
            "user": self.user.username,
            "questions": [question.to_json() for question in self.questions.all()]
        }

    def number_of_answers(self):
        return len(self.solutions.all())

    def user_answered(self, user):
        for solution in self.solutions.all():
            if solution.user == user:
                return True
        return False

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ("-date",)
    
    def __str__(self):
        return self.question

    def __repr__(self):
        return f'<Question: {self.question[:30]}>'
    
    def to_json(self):
        return {
            "question": self.question,
           
            "answers": [answer.to_json() for answer in self.answers.all()]
        }

    

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer  = models.TextField(max_length=1000)
    is_correct = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return self.answer
    
    def __repr__(self):
        return f'<Answer: {self.answer[:30]}>'

    def to_json(self):
        return {
            "answer": self.answer,
            "is_correct": self.is_correct,
        }



class Solution(models.Model):
    quiz = models.ForeignKey(Quiz,related_name="solutions", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="solutions", on_delete=models.CASCADE)
    score = models.DecimalField(default=0.0, max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
    
    def __str__(self):
        return f"Solution to {self.quiz.title[:20]}"
    
    def __repr__(self):
        return f"<Solution: {self.quiz.title[:20]}>"
    
    def save(self, *args, **kwargs):
        self.score = sum([choice.score for choice in self.choices])
        super(Solution, self).save(*args, **kwargs)

class Choice(models.Model):
    user = models.ForeignKey(User, related_name="choices", on_delete=models.CASCADE)
    Solution = models.ForeignKey(Solution,  related_name="choices", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name="user_choice", on_delete=models.CASCADE)
    score = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Correct" if self.answer.is_correct else "Incorrect"
    
    def save(self, *args, **kwargs):
        if self.answer.is_correct:
            self.score = self.question.quiz.score_for_each_question
        super(Choice, self).save(*args, **kwargs)
