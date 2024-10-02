from ..repositories.wfh_request_repository import WfhRequestRepository
from ..models import WfhRequest
from firebase_admin import storage
from datetime import datetime, timedelta

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
        # is_valid, message = self.validate_wfh_request(wfh_request)
        # if is_valid:
        #     request_id = self.wfh_request_repository.add_wfh_request(wfh_request)
        #     return True, request_id
        # else:
        #     return False, message
        return self.wfh_request_repository.add_wfh_request(wfh_request)
        
    def validate_wfh_request(self, staff_id: str, date: str) -> tuple[bool, list[WfhRequest]]:
        # Extract just the date part if a full datetime string is provided
        date = date.split('T')[0]
        
        # Convert the date string to a datetime object
        request_date = datetime.strptime(date, "%Y-%m-%d")
        
        # Get the start and end of the week for the requested date
        week_start = request_date - timedelta(days=request_date.weekday())
        week_end = week_start + timedelta(days=6)

        week_requests = self.wfh_request_repository.get_wfh_requests_by_staff_id_and_date_range(
            staff_id,
            week_start,
            week_end
        )
        # Check if there are already 2 or more WFH requests for the week
        if len(week_requests) >= 2:
            return (False, "You have exceeded the maximum of 2 WFH requests per week.")

        # Check if there's already a WFH request for the same day
        same_day_requests = [req for req in week_requests if req['date'].split('T')[0] == date]
        if same_day_requests:
            return (False, "You already have a WFH request for this day.")

        # If we've passed all checks, the request is valid
        return (True, "")


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