from .base_repository import BaseRepository
from ..models import Delegate

class DelegateRepository(BaseRepository):
    def _get_collection_name(self):
        return "Delegate"

    def add_delegate(self, delegate: Delegate):
        delegate_data = delegate.__dict__
        result = self.add(delegate_data)
        return {"doc_id": result, **delegate_data}

    
    def get_delegate_by_delegate_id(self, delegate_id: int) -> Delegate:
        delegate_data = self.get_by_other_id("delegate_id", delegate_id)
        if delegate_data:
            doc_id = delegate_data.pop("doc_id")  # Remove doc_id from delegate_data
            return {"doc_id": doc_id, **Delegate(**delegate_data).__dict__}  # Include doc_id in the result
        return None
    
    def get_delegate_by_manager_id(self, manager_id: int) -> Delegate:
        delegate_data = self.get_by_other_id("manager_id", manager_id)
        if delegate_data:
            doc_id = delegate_data.pop("doc_id")  # Remove doc_id from delegate_data
            return {"doc_id": doc_id, **Delegate(**delegate_data).__dict__}  # Include doc_id in the result
        return None
    
    def get_all_delegates(self) -> list[Delegate]:
        delegates_data = self.get_all()
        # return [{"delegate_id": delegate_data.pop("doc_id"), **delegate_data} for delegate_data in delegates_data]
        return [{"doc_id": delegate_data["doc_id"], "delegate_id": delegate_data.pop("doc_id"), **delegate_data} for delegate_data in delegates_data]
    
    def update_delegate(self, delegate_id: int, delegate: Delegate):
        delegate_data = delegate.__dict__
        self.update_by_other_id("delegate_id", delegate_id, delegate_data)

    def delete_delegate(self, doc_id: str):
        self.delete(doc_id)
