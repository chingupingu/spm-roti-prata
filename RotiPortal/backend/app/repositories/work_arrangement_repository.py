from .base_repository import BaseRepository

class WorkArrangementRepository(BaseRepository):
    def _get_collection_name(self):
        return "Work arrangements"
    
    def filter_arrangements(self, status=None, staff_id=None, start_date=None, end_date=None):
        query = self.collection
        
        if status:
            query = query.where("Status", "==", status)
        if staff_id:
            query = query.where("Staff_ID", "==", staff_id)  # Assuming Staff_ID is the way to filter by employee
        if start_date and end_date:
            query = query.where("Date", ">=", start_date).where("Date", "<=", end_date)
        
        return query.get()