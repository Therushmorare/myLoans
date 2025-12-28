from loans_project.models.disbursements import Disbursments
from loans_project.models.admin import AdminUser
import uuid
from django.db import transaction
from loans_project.core.functions.logs import log_user_activity
from loans_project.models.service_provider import ServiceProvider
from loans_project.core.functions.cdn_file_upload import *
from loans_project.models.service_provider_files import ProviderFiles

def add_provider_files(admin_id, provider_id, files_arr):
    try:
        #Check admin authorization
        admin = AdminUser.objects.filter(id=admin_id).first()
        if not admin:
            return {'message': 'You are not authorized to perform this action'}, 403

        #Check provider existence
        provider = ServiceProvider.objects.filter(provider_id=provider_id).first()
        if not provider:
            return {'message': 'Service provider does not exist'}, 404

        if not files_arr:
            return {'message': 'No files provided'}, 400

        # Upload files to S3
        upload_results = upload_multiple_files(files_arr, provider_id)

        uploaded = []
        failed = []

        #Save each uploaded file to DB with its own unique file_id
        for file_obj, result in zip(files_arr, upload_results):
            if not result.get("success"):
                failed.append({
                    "file_name": file_obj.name,
                    "error": result.get("error")
                })
                continue

            provider_file = ProviderFiles.objects.create(
                added_by=str(admin_id),
                provider_id=provider_id,
                file_id=uuid.uuid4(),  #unique ID per file
                document=result["url"]
            )

            uploaded.append({
                "file_id": str(provider_file.file_id),
                "document": provider_file.document
            })

        # Return structured response
        return {
            "message": "Files processed",
            "uploaded_count": len(uploaded),
            "failed_count": len(failed),
            "files": uploaded,
            "errors": failed
        }, 200

    except Exception as e:
        print(f"Provider file upload error: {e}")
        return {'message': 'Something went wrong'}, 500
