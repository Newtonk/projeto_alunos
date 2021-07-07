from django.db import models

# Create your models here.

class GraphState(models.Model):
    hashId = models.CharField(max_length=100)
    data = models.CharField(max_length=1000000)

    def __str__(self):
        return self.hashId

