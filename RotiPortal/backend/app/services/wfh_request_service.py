from ..repositories.wfh_request_repository import WfhRequestRepository
from ..models import WfhRequest
from firebase_admin import storage
import uuid

class WfhRequestService:
    def __init__(self):
        self.wfh_request_repository = WfhRequestRepository()

    def create_wfh_request(self, staff_id: str, date: str, shift: str, reason: str, recurring: bool, attachment_file, status: str) -> str:
        if attachment_file:
            # upload attachments to firebase storage
            bucket = storage.bucket()
            blob = bucket.blob(f"wfh_attachments/{staff_id}_{date}_{attachment_file.filename}")
            blob.upload_from_string(
                attachment_file.read(),
                content_type=attachment_file.content_type
            )

            # make blob public
            blob.make_public()

            # Get the public URL
            attachment_url = blob.public_url
        else:
            attachment_url = None
        wfh_request = WfhRequest(staff_id=staff_id, 
                                date=date, 
                                shift=shift,
                                reason=reason,
                                recurring=recurring,
                                attachment_url=attachment_url,
                                status=status
                                )
        return self.wfh_request_repository.add_wfh_request(wfh_request)

    def get_wfh_request(self, request_id: str) -> WfhRequest:
        return self.wfh_request_repository.get_wfh_request(request_id)

    def get_all_wfh_requests(self) -> list[WfhRequest]:
        return self.wfh_request_repository.get_all_wfh_requests()
    
    def get_wfh_requests_by_staff_id(self, staff_id: str) -> list[WfhRequest]:
        return self.wfh_request_repository.get_wfh_requests_by_staff_id(staff_id)
    
    def get_wfh_requests_by_status(self, status: str) -> list[WfhRequest]:
        return self.wfh_request_repository.get_wfh_requests_by_status(status)
    
    def update_wfh_request(self, request_id: str, wfh_request: WfhRequest):
        self.wfh_request_repository.update_wfh_request(request_id, wfh_request)
    
    def delete_wfh_request(self, request_id: str):
        self.wfh_request_repository.delete_wfh_request(request_id)

    def delete_attachment(self, attachment_url):
        if attachment_url:
            bucket = storage.bucket()
            blob = bucket.blob(attachment_url.split('/')[-1])
            blob.delete()

    def upload_attachment(self, file, request_id):
        if file:
            bucket = storage.bucket()
            file_extension = file.filename.split('.')[-1]
            blob_name = f"wfh_attachments/{request_id}_{uuid.uuid4()}.{file_extension}"
            blob = bucket.blob(blob_name)
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )
            return blob.public_url