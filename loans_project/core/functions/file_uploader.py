from models.uploaded_files import Document
import os
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def upload_files(user_id, file):
    try:
        user = User.objects.get(id=user_id)  # get actual User object

        user_folder = os.path.join(settings.MEDIA_ROOT, str(user_id))
        os.makedirs(user_folder, exist_ok=True)
        
        file_path = os.path.join(user_folder, file.name)
        
        # save file manually
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Save in DB
        upload = Document.objects.create(user=user, file=file_path)
        return upload

    except Exception as e:
        print(f"File save error: {e}")
        return None