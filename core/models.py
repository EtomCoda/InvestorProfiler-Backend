from django.db import models

class Question(models.Model):
    TEXT_CATEGORIES = (
        ('TIME', 'Time Horizon'),
        ('TOLERANCE', 'Risk Tolerance'),
    )
    text = models.TextField()
    order = models.PositiveIntegerField(unique=True)
    category = models.CharField(max_length=10, choices=TEXT_CATEGORIES)

    def __str__(self):
        return f"{self.order}. {self.text}"

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.TextField()
    score = models.IntegerField()

    def __str__(self):
        return f"Q{self.question.order} - {self.text} ({self.score})"

class RiskProfile(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProfileMapping(models.Model):
    time_score_min = models.IntegerField()
    time_score_max = models.IntegerField()
    tolerance_score_min = models.IntegerField()
    tolerance_score_max = models.IntegerField()
    profile = models.ForeignKey(RiskProfile, on_delete=models.CASCADE)

    def matches(self, time_score, tolerance_score):
        return self.time_score_min <= time_score <= self.time_score_max and \
               self.tolerance_score_min <= tolerance_score <= self.tolerance_score_max

    def __str__(self):
        return f"{self.time_score_min}-{self.time_score_max} | {self.tolerance_score_min}-{self.tolerance_score_max} → {self.profile.name}"
