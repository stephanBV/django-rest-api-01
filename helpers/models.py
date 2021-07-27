from django.db import models

class TrackingModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True #when inherited, it does not generate a database table or have a manager, and cannot be instantiated or saved directly.
        ordering=('-created_at',) # ordering in descending order (-)