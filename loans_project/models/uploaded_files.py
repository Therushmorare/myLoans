from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')  # files go to MEDIA_ROOT/uploads/
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.file.name}"