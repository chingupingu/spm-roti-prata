from ..repositories.work_arrangement_repository import WorkArrangementRepository

class WorkArrangementService:
    def __init__(self):
        self.work_arrangement_repository = WorkArrangementRepository()
    
    def filter_arrangements(self, status=None, staff_id=None, start_date=None, end_date=None):
        arrangements = self.work_arrangement_repository.filter_arrangements(status, staff_id, start_date, end_date)
        return [arrangement.to_dict() for arrangement in arrangements]  # Assuming to_dict() converts the document to a dictionary