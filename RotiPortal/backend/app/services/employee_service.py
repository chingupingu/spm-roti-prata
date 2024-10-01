from ..repositories.employee_repository import EmployeeRepository
from ..models import Employee

class EmployeeService:
    def __init__(self):
        self.employee_repository = EmployeeRepository()

    def create_employee(self, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role) -> str:
        employee = Employee(Staff_FName=Staff_FName, 
                            Staff_LName=Staff_LName, 
                            Dept=Dept, 
                            Position=Position, 
                            Country=Country, 
                            Email=Email, 
                            Reporting_Manager=Reporting_Manager, 
                            Role=Role
                            )
        return self.employee_repository.add_employee(employee)
    
    def get_employee(self, staff_id: str) -> Employee:
        return self.employee_repository.get_employee(staff_id)
    
    def update_employee(self, staff_id: str, employee: Employee):
        self.employee_repository.update_employee(staff_id, employee)

    def delete_employee(self, staff_id: str):
        self.employee_repository.delete_employee(staff_id)

    def get_all_employees(self) -> list[Employee]:
        return self.employee_repository.get_all_employees()

    def get_employee_by_email(self, email: str) -> Employee:
        return self.employee_repository.get_employee_by_email(email)