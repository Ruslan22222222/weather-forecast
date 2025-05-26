from django.db import models
from django.contrib.auth.models import User


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=1)
    last_search = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.city}"

    class Meta:
        ordering = ['-last_search']
        unique_together = ['user', 'city']
