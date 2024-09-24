from .base_repository import BaseRepository
from ..models import Employee

class EmployeeRepository(BaseRepository):
    def _get_collection_name(self):
        return "Employee"
    
    def add_employee(self, employee: Employee):
        employee_data = employee.__dict__
        return self.add(employee_data)
    
    def get_employee(self, doc_id: str) -> Employee:
        employee_data = self.get(doc_id)
        if employee_data:
            employee_data['doc_id'] = doc_id
            return Employee(**employee_data)
        return None
    
    def update_employee(self, employee: Employee):
        employee_data = employee.__dict__
        doc_id = employee_data.pop('doc_id')
        self.update(doc_id, employee_data)

    def delete_employee(self, doc_id: str):
        self.delete(doc_id)

    def get_all_employees(self) -> list[Employee]:
        employees_data = self.get_all()
        return [Employee(**employee_data) for employee_data in employees_data]