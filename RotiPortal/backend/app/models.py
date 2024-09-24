import itertools

class Employee:

    id_iter = itertools.count()
    
    def __init__(self, Staff_ID, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role, doc_id=None):
        # self.Staff_ID = next(Employee.id_iter)
        self.Staff_ID = Staff_ID
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Dept = Dept
        self.Position = Position
        self.Country = Country
        self.Email = Email
        self.Reporting_Manager = Reporting_Manager
        self.Role = Role
        self.doc_id = doc_id

    @staticmethod
    def __repr__(self):
        return f"Employee(\
                doc_id={self.doc_id}, \
                Staff_ID={self.Staff_ID}, \
                Staff_FName={self.Staff_FName}, \
                Staff_LName={self.Staff_LName}, \
                Dept={self.Dept}, \
                Position={self.Position}, \
                Email={self.Email}, \
                Reporting_Manager={self.Reporting_Manager}, \
                Role={self.Role}\
            )"