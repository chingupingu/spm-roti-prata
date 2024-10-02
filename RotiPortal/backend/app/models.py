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
    def __init__(self, staff_id, date, shift, reason, recurring, attachment_url, status):
        self.staff_id = staff_id
        self.date = date
        self.shift = shift
        self.reason = reason
        self.recurring = recurring
        self.attachment_url = attachment_url
        self.status = status

    @staticmethod
    def __repr__(self):
        return f"WfhRequest(\
                staff_id={self.staff_id}, \
                date={self.date}, \
                shift={self.shift}, \
                reason={self.reason}, \
                recurring={self.recurring}, \
                attachment_url={self.attachment_url}\
                status={self.status}\
            )"

                
class Schedule:
    # id_iter = itertools.count()
    def __init__(self, Staff_ID, Date, Duration, Status, Work_Arrangement, doc_id=None):
        self.Staff_ID = Staff_ID
        self.Date = Date
        self.Duration = Duration
        self.Status = Status
        self.Work_Arrangement = Work_Arrangement

    @staticmethod
    def __repr__(self):
        return f"Schedule(\
                doc_id={self.doc_id}, \
                Staff_ID={self.Staff_ID}, \
                Date={self.Date}, \
                Duration={self.Duration}, \
                Status={self.Status}, \
                Work_Arrangement={self.Work_Arrangement}\
            )"