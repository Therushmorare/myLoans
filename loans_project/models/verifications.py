from django.db import models
import uuid

class Verifications(models.Model):
    user_id = models.UUIDField()
    id_number = models.CharField(max_length=13)
    source = models.CharField(max_length=10)  # API | LOCAL
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_id", "id_number")
