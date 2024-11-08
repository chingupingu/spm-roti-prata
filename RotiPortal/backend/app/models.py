class Employee:
    # id_iter = itertools.count()
    def __init__(self, Staff_FName, Staff_LName, Dept, Position, Country, Email, Reporting_Manager, Role):
        self.Staff_FName = Staff_FName
        self.Staff_LName = Staff_LName
        self.Dept = Dept
        self.Position = Position
        self.Country = Country
        self.Email = Email
        self.Reporting_Manager = Reporting_Manager
        self.Role = Role

    @staticmethod
    def __repr__(self):
        return f"Employee(\
                Staff_FName={self.Staff_FName}, \
                Staff_LName={self.Staff_LName}, \
                Dept={self.Dept}, \
                Position={self.Position}, \
                Email={self.Email}, \
                Reporting_Manager={self.Reporting_Manager}, \
                Role={self.Role}\
            )"


class WfhRequest:
    def __init__(self, staff_id, date, shift, reason, recurring, attachment_url, status, comment="", approving_manager=""):
        self.staff_id = staff_id
        self.date = date
        self.shift = shift
        self.reason = reason
        self.recurring = recurring
        self.attachment_url = attachment_url
        self.status = status
        self.comment = comment
        self.approving_manager = approving_manager

    @staticmethod
    def __repr__(self):
        return f"WfhRequest(\
                staff_id={self.staff_id}, \
                date={self.date}, \
                shift={self.shift}, \
                reason={self.reason}, \
                recurring={self.recurring}, \
                attachment_url={self.attachment_url}, \
                status={self.status}, \
                comment={self.comment}, \
                approving_manager={self.approving_manager}\
            )"

class Delegate:
    def __init__(self, manager_id, delegate_id, start_date, end_date, dept):
        self.manager_id = manager_id
        self.delegate_id = delegate_id
        self.start_date = start_date
        self.end_date = end_date
        self.dept = dept

