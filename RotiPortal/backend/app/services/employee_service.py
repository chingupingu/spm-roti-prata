from ..repositories.employee_repository import EmployeeRepository
from ..models import Employee

class EmployeeService:
    def __init__(self):
        self.employee_repository = EmployeeRepository()

    def create_employee(self, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role) -> str:
        employee = Employee(doc_id=None, 
                            Staff_FName=Staff_FName, 
                            Staff_LName=Staff_LName, 
                            Dept=Dept, 
                            Position=Position, 
                            Country=Country, 
                            Email=Email, 
                            Reporting_Manager=Reporting_Manager, 
                            Role=Role
                            )
        return self.employee_repository.add_employee(employee)
    
    def get_employee(self, doc_id: str) -> Employee:
        return self.employee_repository.get_employee(doc_id)
    
    def update_employee(self, employee: Employee):
        self.employee_repository.update_employee(employee)

    def delete_employee(self, doc_id: str):
        self.employee_repository.delete_employee(doc_id)

    def get_all_employees(self) -> list[Employee]:
        return self.employee_repository.get_all_employees()