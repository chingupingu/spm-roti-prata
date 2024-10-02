from ..repositories.schedule_repository import ScheduleRepository
from ..models import Schedule

class ScheduleService:
    def __init__(self):
        self.schedule_repository = ScheduleRepository()

    def create_schedule(self, Staff_ID, Date, Duration, Status, Work_Arrangement) -> str:
        schedule = Schedule(doc_id=None, 
                            Staff_ID=Staff_ID, 
                            Date=Date, 
                            Duration=Duration, 
                            Status=Status, 
                            Work_Arrangement=Work_Arrangement
                            )
        return self.schedule_repository.add_schedule(schedule)
    
    def get_schedule(self, doc_id: str) -> list[Schedule]:
        return self.schedule_repository.get_schedule(doc_id)
    
    def update_schedule(self, schedule: Schedule):
        self.schedule_repository.update_schedule(schedule)

    def delete_schedule(self, doc_id: str):
        self.schedule_repository.delete_schedule(doc_id)

    def get_all_schedules(self) -> list[Schedule]:
        return self.schedule_repository.get_all_schedules()