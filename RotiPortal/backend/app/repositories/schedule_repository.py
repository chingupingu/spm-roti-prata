from .base_repository import BaseRepository
from ..models import Schedule

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
    
    def update_schedule(self, schedule: Schedule):
        schedule_data = schedule.__dict__
        doc_id = schedule_data.pop('doc_id')
        self.update(doc_id, schedule_data)

    def delete_schedule(self, doc_id: str):
        self.delete(doc_id)

    def get_all_schedules(self) -> list[Schedule]:
        schedules_data = self.get_all()
        return [Schedule(**schedule_data) for schedule_data in schedules_data]
    
    def get_schedules_and_employees_by_dept(self, dept: str) -> dict:
        # Step 1: Fetch employees by department
        employee_docs = self.db.collection('Employee').where('Dept', '==', dept).stream()
        
        # Create a dictionary with first name as the key
        employees = {}
        staff_ids = []
        for doc in employee_docs:
            first_name = doc.get('Staff_FName')
            staff_id = doc.id
            staff_ids.append(staff_id)

            if first_name not in employees:
                employees[first_name] = {
                    "Staff_ID": staff_id,
                    "Last_Name": doc.get('Staff_LName'),
                    "Email": doc.get('Email'),
                    "Position": doc.get('Position'),
                    "Dept": doc.get('Dept'),
                    "Schedules": []
                }

        # Step 2: If no employees are found, return an empty result
        if not staff_ids:
            return {}

        # Step 3: Retrieve schedules for the employees
        schedules_data = self.db.collection('Schedule').where('Staff_ID', 'in', staff_ids).stream()

        # Step 4: Group schedules under each employee's first name
        for schedule_doc in schedules_data:
            schedule = schedule_doc.to_dict()
            staff_id = schedule.get('Staff_ID')

            # Find the employee's first name by their Staff_ID
            for first_name, employee in employees.items():
                if employee["Staff_ID"] == staff_id:
                    # Append the schedule to the respective employee
                    employee["Schedules"].append({
                        "Date": schedule.get('Date'),
                        "Duration": schedule.get('Duration'),
                        "Work_Arrangement": schedule.get('Work_Arrangement'),
                        "Status": schedule.get('Status')
                    })
                    break

        # Step 5: Format the result as a dictionary with first names as keys
        result = {first_name: employee["Schedules"] for first_name, employee in employees.items()}
        
        return result