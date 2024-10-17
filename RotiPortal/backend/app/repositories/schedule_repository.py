from .base_repository import BaseRepository
from ..models import Schedule
from datetime import datetime

class ScheduleRepository(BaseRepository):
    def _get_collection_name(self):
        return "Schedule"
    
    def add_schedule(self, schedule: Schedule):
        schedule_data = schedule.__dict__
        return self.add(schedule_data)
    
    def get_schedule(self, doc_id: str) -> list[Schedule]:
        all_schedules = self.get_all()
        filtered_schedules = [Schedule(**schedule_data) for schedule_data in all_schedules if schedule_data['Staff_ID'] == doc_id]
        return filtered_schedules
    
    def get_all_schedules(self) -> list[Schedule]:
        schedules_data = self.get_all()
        return [Schedule(**schedule_data) for schedule_data in schedules_data]
    
    def get_schedules_by_date(self, date: str) -> list[Schedule]:
        schedules_data = self.get_all()
        filtered_schedules = [
            Schedule(**schedule_data) 
            for schedule_data in schedules_data 
            if schedule_data['Date'] == date
        ]
        return filtered_schedules

    def update_schedule(self, schedule: Schedule):
        schedule_data = schedule.__dict__
        doc_id = schedule_data.pop('doc_id')
        self.update(doc_id, schedule_data)

    def delete_schedule(self, doc_id: str):
        self.delete(doc_id)
