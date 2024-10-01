from .base_repository import BaseRepository
from ..models import Employee

class EmployeeRepository(BaseRepository):
    def _get_collection_name(self):
        return "Employee"

    def add_employee(self, employee: Employee):
        employee_data = employee.__dict__
        return self.add(employee_data)
    
    def get_employee(self, staff_id: str) -> Employee:
        employee_data = self.get(staff_id)
        if employee_data:
            # employee_data['Staff_ID'] = staff_id
            return Employee(**employee_data)
        return None
    
    def update_employee(self, staff_id: str, employee: Employee):
        employee_data = employee.__dict__
        # doc_id = employee_data.pop('Staff_ID')
        self.update(staff_id, employee_data)

    def delete_employee(self, doc_id: str):
        self.delete(doc_id)

    def get_all_employees(self) -> list[Employee]:
        employees_data = self.get_all()
        # return [Employee(**employee_data) for employee_data in employees_data]
        return [{"Staff_ID": employee_data.pop('Staff_ID'), **employee_data} for employee_data in employees_data]