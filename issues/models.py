from django.db import models
from django.contrib.auth.models import User

class Issue(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    LOCATION_CHOICES = [
        ('Kimberley CBD', 'Kimberley CBD'),
        ('Galeshewe', 'Galeshewe'),
        ('Roodepan', 'Roodepan'),
        ('Cassandra', 'Cassandra'),
        ('Homevale', 'Homevale'),
        ('New Park', 'New Park'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Kimberley CBD')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title