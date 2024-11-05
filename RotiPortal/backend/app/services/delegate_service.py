from ..repositories.delegate_repository import DelegateRepository
from ..models import Delegate

class DelegateService:
    def __init__(self):
        self.delegate_repository = DelegateRepository()

    def create_delegate(self, manager_id, delegate_id, start_date, end_date, dept) -> str:
        delegate = Delegate(manager_id, delegate_id, start_date, end_date, dept)
        return self.delegate_repository.add_delegate(delegate)

    def get_delegate_by_delegate_id(self, delegate_id: int) -> Delegate:
        return self.delegate_repository.get_delegate_by_delegate_id(delegate_id)
    
    def get_delegate_by_manager_id(self, manager_id: int) -> Delegate:
        return self.delegate_repository.get_delegate_by_manager_id(manager_id)
    
    def get_all_delegates(self) -> list[Delegate]:
        return self.delegate_repository.get_all_delegates()

    def update_delegate(self, delegate_id: int, delegate: Delegate):
        self.delegate_repository.update_delegate(delegate_id, delegate)

    def delete_delegate(self, doc_id: str):
        self.delegate_repository.delete_delegate(doc_id)
