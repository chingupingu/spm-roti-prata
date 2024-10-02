from .base_repository import BaseRepository
from ..models import Schedule

class ScheduleRepository(BaseRepository):
    def _get_collection_name(self):
        return "Schedule"
    
    def add_schedule(self, schedule: Schedule):
        schedule_data = schedule.__dict__
        return self.add(schedule_data)
    
    def get_schedule(self, doc_id: str) -> Schedule:
        schedule_data = self.get(doc_id)
        if schedule_data:
            schedule_data['doc_id'] = doc_id
            return Schedule(**schedule_data)
        return None
    
    def update_schedule(self, schedule: Schedule):
        schedule_data = schedule.__dict__
        doc_id = schedule_data.pop('doc_id')
        self.update(doc_id, schedule_data)

    def delete_schedule(self, doc_id: str):
        self.delete(doc_id)

    def get_all_schedules(self) -> list[Schedule]:
        schedules_data = self.get_all()
        return [Schedule(**schedule_data) for schedule_data in schedules_data]