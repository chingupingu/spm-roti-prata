from .base_repository import BaseRepository
from ..models import WfhRequest

class WfhRequestRepository(BaseRepository):
    def _get_collection_name(self):
        return "WfhRequest"

    def add_wfh_request(self, wfh_request: WfhRequest):
        wfh_request_data = wfh_request.__dict__
        return self.add(wfh_request_data)
    
    def get_wfh_request(self, request_id: str) -> WfhRequest:
        wfh_request_data = self.get(request_id)
        if wfh_request_data:
            return WfhRequest(**wfh_request_data)
        return None
    
    def get_all_wfh_requests(self) -> list[WfhRequest]:
        wfh_requests_data = self.get_all()
        return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data} for wfh_request_data in wfh_requests_data]
    
    def get_wfh_requests_by_staff_id(self, staff_id: str) -> list[WfhRequest]:
        wfh_requests_data = self.get_all()
        # for wfh_request_data in wfh_requests_data:
        #     if wfh_request_data.get('staff_id') == staff_id:
        #         return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data}]
        # return None
        return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data} for wfh_request_data in wfh_requests_data if wfh_request_data.get('staff_id') == staff_id]
    
    def get_wfh_requests_by_status(self, status: str) -> list[WfhRequest]:
        wfh_requests_data = self.get_all()
        # for wfh_request_data in wfh_requests_data:
        #     if wfh_request_data.get('status') == status:
        #         return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data}]
        # return None
        return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data} for wfh_request_data in wfh_requests_data if wfh_request_data.get('status') == status]

    def update_wfh_request(self, request_id: str, wfh_request: WfhRequest):
        wfh_request_data = wfh_request.__dict__
        self.update(request_id, wfh_request_data)

    def delete_wfh_request(self, request_id: str):
        self.delete(request_id)