from django.contrib.auth.models import User
from django.db import models


# Modelo de tareas
class Task(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    date_complete = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
            Devuelve una representación en cadena del objeto.
        """
        return self.title + ' ' + self.user.username
