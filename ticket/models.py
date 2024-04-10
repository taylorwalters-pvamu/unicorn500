from django.db import models

# Create your models here.
class SupportTicket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SupportTicketAdmin(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Closed', 'Closed')])
    priority = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    submission_date = models.DateTimeField(auto_now_add=True)
    resolution_date = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.title