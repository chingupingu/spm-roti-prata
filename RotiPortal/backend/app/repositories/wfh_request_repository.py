from .base_repository import BaseRepository
from ..models import WfhRequest
from datetime import datetime

class WfhRequestRepository(BaseRepository):
    def _get_collection_name(self):
        return "WfhRequest"

    def add_wfh_request(self, wfh_request: WfhRequest):
        wfh_request_data = wfh_request.__dict__
        return self.add(wfh_request_data)
    
    def get_wfh_request(self, request_id: str) -> WfhRequest:
        wfh_request_data = self.get(request_id)
        if wfh_request_data:
            return WfhRequest(**wfh_request_data)
        return None
    
    def get_all_wfh_requests(self) -> list[WfhRequest]:
        wfh_requests_data = self.get_all()
        return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data} for wfh_request_data in wfh_requests_data]
    
    def get_wfh_requests_by_staff_id(self, staff_id: str) -> list[WfhRequest]:
        wfh_requests_data = self.get_all()
        # for wfh_request_data in wfh_requests_data:
        #     if wfh_request_data.get('staff_id') == staff_id:
        #         return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data}]
        # return None
        return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data} for wfh_request_data in wfh_requests_data if wfh_request_data.get('staff_id') == staff_id]
    
    def get_wfh_requests_by_status(self, status: str) -> list[WfhRequest]:
        wfh_requests_data = self.get_all()
        # for wfh_request_data in wfh_requests_data:
        #     if wfh_request_data.get('status') == status:
        #         return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data}]
        # return None
        return [{"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data} for wfh_request_data in wfh_requests_data if wfh_request_data.get('status') == status]

    def update_wfh_request(self, request_id: str, wfh_request: WfhRequest):
        wfh_request_data = wfh_request.__dict__
        self.update(request_id, wfh_request_data)

    def delete_wfh_request(self, request_id: str):
        self.delete(request_id)

    def get_wfh_requests_by_staff_id_and_date_range(self, staff_id: str, start_date: datetime, end_date: datetime) -> list[WfhRequest]:
        wfh_requests_data = self.get_all()
        filtered_requests = []
        for wfh_request_data in wfh_requests_data:
            if wfh_request_data.get('staff_id') == staff_id:
                request_date_str = wfh_request_data.get('date')
                request_date = datetime.strptime(request_date_str.split('T')[0], "%Y-%m-%d")
                if start_date <= request_date <= end_date:
                    filtered_requests.append({"request_id": wfh_request_data.pop("doc_id"), **wfh_request_data})
        return filtered_requests

    def get_schedules_and_employees_by_dept(self, dept: str, role: str) -> dict:
        if (dept == "CEO") :
            employee_docs = self.db.collection('Employee').stream()
        else :
            employee_docs = self.db.collection('Employee').where('Dept', '==', dept).stream()

        # Create a dictionary with first name as the key
        employees = {}
        staff_ids = []

        if dept == "CEO" :
            for doc in employee_docs:
                first_name = doc.get('Staff_FName')
                staff_role = doc.get('Role')
                staff_position = doc.get('Position')
                staff_id = doc.id
                staff_ids.append(staff_id)

                if first_name not in employees and staff_role == 1 and staff_position != "HR Team":
                    employees[first_name] = {
                        "Staff_ID": staff_id,
                        "Schedules": []
                    }
        elif role == "2" :
            for doc in employee_docs:
                first_name = doc.get('Staff_FName')
                staff_role = doc.get('Role')
                staff_id = doc.id
                staff_ids.append(staff_id)

                if first_name not in employees and staff_role != 1 and staff_role != 3:
                    employees[first_name] = {
                        "Staff_ID": staff_id,
                        "Schedules": []
                    }
        elif role == "3":
            for doc in employee_docs:
                first_name = doc.get('Staff_FName')
                staff_role = doc.get('Role')
                staff_id = doc.id
                staff_ids.append(staff_id)

                if first_name not in employees and staff_role != 1:
                    employees[first_name] = {
                        "Staff_ID": staff_id,
                        "Schedules": []
                    }
        else :
            for doc in employee_docs:
                first_name = doc.get('Staff_FName')
                staff_id = doc.id
                staff_ids.append(staff_id)

                if first_name not in employees:
                    employees[first_name] = {
                        "Staff_ID": staff_id,
                        "Schedules": []
                    }

        # Step 2: If no employees are found, return an empty result
        if not staff_ids:
            return {}

        # Step 3: Retrieve schedules for the employees
        schedules_data = []
        batch_size = 30

        for i in range(0, len(staff_ids), batch_size):
            batch_ids = staff_ids[i:i + batch_size]
            batch_schedules = self.db.collection('WfhRequest').where('staff_id', 'in', batch_ids).stream()
            schedules_data.extend(batch_schedules)

        # Step 4: Group schedules under each employee's first name
        for schedule_doc in schedules_data:
            schedule = schedule_doc.to_dict()
            staff_id = schedule.get('staff_id')

            # Find the employee's first name by their Staff_ID
            for first_name, employee in employees.items():
                if employee["Staff_ID"] == staff_id:
                    # Append the schedule to the respective employee
                    employee["Schedules"].append({
                        "Date": schedule.get('date'),
                        "Duration": schedule.get('shift'),
                        "Work_Arrangement": 'Work from Home',
                        "Status": schedule.get('status')
                    })
                    break

        # Step 5: Format the result as a dictionary with first names as keys
        result = {first_name: employee["Schedules"] for first_name, employee in employees.items()}

        return result