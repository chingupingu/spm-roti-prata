from ..repositories.wfh_request_repository import WfhRequestRepository
from ..models import WfhRequest
from firebase_admin import storage
from datetime import datetime, timedelta
from ..services.employee_service import EmployeeService

class WfhRequestService:
    def __init__(self):
        self.wfh_request_repository = WfhRequestRepository()
        self.employee_service = EmployeeService()


    def create_wfh_request(self, staff_id: str, dates: list[str], shift: str, reason: str, recurring: bool, attachment_file, status: str, comment: str = "", approving_manager: str = "") -> str:
        successful_requests = []
        
        # Handle the attachment only if provided
        attachment_url = None
        if attachment_file:
            # Upload attachments to Firebase storage
            bucket = storage.bucket()
            blob = bucket.blob(f"wfh_attachments/{staff_id}_{date}_{attachment_file.filename}")
            blob.upload_from_string(
                attachment_file.read(),
                content_type=attachment_file.content_type
            )
            
            # Make blob public
            blob.make_public()
            
            # Get the public URL
            attachment_url = blob.public_url

        # Iterate over each date
        for date in dates:
            wfh_request = WfhRequest(
                staff_id=staff_id,
                date=date,
                shift=shift,
                reason=reason,
                recurring=recurring,
                attachment_url=attachment_url,
                status=status,
                comment=comment,
                approving_manager=approving_manager
            )
            
            # Add the WFH request to the repository
            request_id = self.wfh_request_repository.add_wfh_request(wfh_request)
            
            # Collect successful request IDs (or any other success criteria)
            if request_id:  # Assuming that a non-falsy value indicates success
                successful_requests.append(request_id)

        # Check if all requests were successful
        if len(successful_requests) == len(dates):
            return True  # Return True
        else:
            return False, "Some requests could not be processed."  # Return failure message


    # # OLD create_wfh_request
    # def create_wfh_request(self, staff_id: str, date: str, shift: str, reason: str, recurring: bool, attachment_file, status: str, comment: str = "") -> str:
    #     if attachment_file:
    #         # upload attachments to firebase storage
    #         bucket = storage.bucket()
    #         blob = bucket.blob(f"wfh_attachments/{staff_id}_{date}_{attachment_file.filename}")
    #         blob.upload_from_string(
    #             attachment_file.read(),
    #             content_type=attachment_file.content_type
    #         )

    #         # make blob public
    #         blob.make_public()

    #         # Get the public URL
    #         attachment_url = blob.public_url
    #     else:
    #         attachment_url = None
    #     wfh_request = WfhRequest(staff_id=staff_id, 
    #                             date=date, 
    #                             shift=shift,
    #                             reason=reason,
    #                             recurring=recurring,
    #                             attachment_url=attachment_url,
    #                             status=status,
    #                             comment=comment,
    #                             )
    #     # is_valid, message = self.validate_wfh_request(wfh_request)
    #     # if is_valid:
    #     #     request_id = self.wfh_request_repository.add_wfh_request(wfh_request)
    #     #     return True, request_id
    #     # else:
    #     #     return False, message
    #     return self.wfh_request_repository.add_wfh_request(wfh_request)
        
    # def validate_wfh_request(self, staff_id: str, date: str) -> tuple[bool, list[WfhRequest]]:
    #     # Extract just the date part if a full datetime string is provided
    #     date = date.split('T')[0]
        
    #     # Convert the date string to a datetime object
    #     request_date = datetime.strptime(date, "%Y-%m-%d")
        
    #     # Get the start and end of the week for the requested date
    #     week_start = request_date - timedelta(days=request_date.weekday())
    #     week_end = week_start + timedelta(days=6)

    #     week_requests = self.wfh_request_repository.get_wfh_requests_by_staff_id_and_date_range(
    #         staff_id,
    #         week_start,
    #         week_end
    #     )
    #     # Check if there are already 2 or more WFH requests for the week
    #     if len(week_requests) >= 2:
    #         return (True, "You have exceeded the maximum of 2 WFH requests per week.")

    #     # Check if there's already a WFH request for the same day
    #     same_day_requests = [req for req in week_requests if req['date'].split('T')[0] == date]
    #     if same_day_requests:
    #         return (False, "You already have a WFH request for this day.")

    #     # If we've passed all checks, the request is valid
    #     return (True, "")

    def validate_wfh_request(self, staff_id: str, dates: list[str]) -> tuple[bool, list[str]]:
        import pytz
        messages = []
        valid = True

        for date in dates:
            # Extract just the date part if a full datetime string is provided
            date_to_format_later = date
            date = date.split('T')[0]
            
            # Convert the date string to a datetime object
            request_date = datetime.strptime(date, "%Y-%m-%d")
            
            # Get the start and end of the week for the requested date
            week_start = request_date - timedelta(days=request_date.weekday())
            week_end = week_start + timedelta(days=6)

            week_requests = self.wfh_request_repository.get_wfh_requests_by_staff_id_and_date_range(
                staff_id,
                week_start,
                week_end
            )

            # Check if there are already 2 or more WFH requests for the week
            if len(week_requests) >= 2:
                # Original ISO 8601 date string
                iso_date = date_to_format_later

                # Convert to a datetime object in UTC
                dt_utc = datetime.fromisoformat(iso_date[:-1])  # Remove the 'Z' for compatibility
                dt_utc = dt_utc.replace(tzinfo=pytz.utc)  # Set timezone to UTC

                # Convert to Singapore timezone
                singapore_tz = pytz.timezone('Asia/Singapore')
                dt_singapore = dt_utc.astimezone(singapore_tz)

                # Format to dd-mm-yyyy
                formatted_date = dt_singapore.strftime("%d-%m-%Y")
                messages.append("You have exceeded the maximum of 2 WFH requests per week for the week of " + formatted_date)
                valid = True

            # Check if there's already a WFH request for the same day
            same_day_requests = [req for req in week_requests if req['date'].split('T')[0] == date]
            if same_day_requests:
                # Original ISO 8601 date string
                iso_date = date_to_format_later

                # Convert to a datetime object in UTC
                dt_utc = datetime.fromisoformat(iso_date[:-1])  # Remove the 'Z' for compatibility
                dt_utc = dt_utc.replace(tzinfo=pytz.utc)  # Set timezone to UTC

                # Convert to Singapore timezone
                singapore_tz = pytz.timezone('Asia/Singapore')
                dt_singapore = dt_utc.astimezone(singapore_tz)

                # Format to dd-mm-yyyy
                formatted_date = dt_singapore.strftime("%d-%m-%Y")
                messages.append("You already have a WFH request for this day: " + formatted_date)
                valid = False
        
        if (messages == []):
            messages = ""

        if valid:
            return (True, messages)

        return (False, messages)

    # New alert_supervisor method
    def alert_supervisor(self, staff_id: str, dates: list[str], shift: str, reason: str) -> None:
        import pytz

        # Getting names
        employee_object = self.employee_service.get_employee(staff_id)
        employee_name = employee_object.Staff_FName + " " + employee_object.Staff_LName
        reporting_manager_id = employee_object.Reporting_Manager
        reporting_manager_object = self.employee_service.get_employee(reporting_manager_id)
        reporting_manager_name = reporting_manager_object.Staff_FName + " " + reporting_manager_object.Staff_LName
        if len(dates) == 1:
            # Non-recurring
            date = dates[0]
            recurring = False
        else:
            # Recurring
            recurring = True

        if shift == "FD":
            shift = "Full Day"

        # If non-recurring
        if (not recurring):
            # Original ISO 8601 date string
            iso_date = date

            # Convert to a datetime object in UTC
            dt_utc = datetime.fromisoformat(iso_date[:-1])  # Remove the 'Z' for compatibility
            dt_utc = dt_utc.replace(tzinfo=pytz.utc)  # Set timezone to UTC

            # Convert to Singapore timezone
            singapore_tz = pytz.timezone('Asia/Singapore')
            dt_singapore = dt_utc.astimezone(singapore_tz)

            # Format to dd-mm-yyyy
            formatted_date = dt_singapore.strftime("%d-%m-%Y")
        # Additional logic for processing the non-recurring will go here...
            message = f"""Subject: New WFH Request from {employee_name}

Hi {reporting_manager_name},

    This email is to inform you of a new work-from-home request submitted by {employee_name}.

    Request Details:
    - Date to WFH: {formatted_date}
    - Shift: {shift}
    - Reason: {reason}

    Please review and respond accordingly.

Thank you,
WFH System"""

        # If recurring
        if (recurring):
            formatted_dates = []
            for date in dates:
                # Original ISO 8601 date string
                iso_date = date

                # Convert to a datetime object in UTC
                dt_utc = datetime.fromisoformat(iso_date[:-1])  # Remove the 'Z' for compatibility
                dt_utc = dt_utc.replace(tzinfo=pytz.utc)  # Set timezone to UTC

                # Convert to Singapore timezone
                singapore_tz = pytz.timezone('Asia/Singapore')
                dt_singapore = dt_utc.astimezone(singapore_tz)

                # Format to dd-mm-yyyy
                formatted_date = dt_singapore.strftime("%d-%m-%Y")
                formatted_dates.append(formatted_date)

            message = f"""Subject: New WFH Request from {employee_name}
Hi {reporting_manager_name},

    This email is to inform you of a new work-from-home request submitted by {employee_name}.
    Note that this is a recurring WFH Request.

    Request Details:
    - Dates to WFH: {formatted_dates}
    - Shift: {shift}
    - Reason: {reason}

    Please review and respond accordingly.

Thank you,
WFH System"""
        self.send_email("innocentstriker1@gmail.com", message)

    # New alert_supervisor method
    def alert_delegate(self, staff_id: str, delegate_id: str, startDate: str, endDate: str) -> None:
        import pytz

        # Getting names
        employee_object = self.employee_service.get_employee(staff_id)
        employee_name = employee_object.Staff_FName + " " + employee_object.Staff_LName
        delegate_manager_object = self.employee_service.get_employee(delegate_id)
        reporting_manager_name = delegate_manager_object.Staff_FName + " " + delegate_manager_object.Staff_LName
        
        # Original ISO 8601 date string
        iso_date = startDate

        # Convert to a datetime object in UTC
        dt_utc = datetime.fromisoformat(iso_date[:-1])  # Remove the 'Z' for compatibility
        dt_utc = dt_utc.replace(tzinfo=pytz.utc)  # Set timezone to UTC

        # Convert to Singapore timezone
        singapore_tz = pytz.timezone('Asia/Singapore')
        dt_singapore = dt_utc.astimezone(singapore_tz)

        # Format to dd-mm-yyyy
        formatted_date = dt_singapore.strftime("%d-%m-%Y")

        # Original ISO 8601 date string
        iso_date2 = endDate

        # Convert to a datetime object in UTC
        dt_utc2 = datetime.fromisoformat(iso_date2[:-1])  # Remove the 'Z' for compatibility
        dt_utc2 = dt_utc2.replace(tzinfo=pytz.utc)  # Set timezone to UTC

        # Convert to Singapore timezone
        singapore_tz = pytz.timezone('Asia/Singapore')
        dt_singapore = dt_utc2.astimezone(singapore_tz)

        # Format to dd-mm-yyyy
        formatted_date2 = dt_singapore.strftime("%d-%m-%Y")
        
        # Additional logic for processing the non-recurring will go here...
        message = f"""Subject: New Delegation from {employee_name}

Hi {reporting_manager_name},

    This email is to inform you have to delegated by {employee_name} to help manage WFH Request from {formatted_date} to {formatted_date2}.

    Do assist accordingly.

Thank you,
WFH System"""

        
        self.send_email("innocentstriker1@gmail.com", message)
    
    # Old alert_supervisor method
#     def alert_supervisor(self, staff_id: str, date: str, shift: str, reason: str) -> None:
#         import pytz

#         employee_object = self.employee_service.get_employee(staff_id)
#         employee_name = employee_object.Staff_FName + " " + employee_object.Staff_LName
#         reporting_manager_id = employee_object.Reporting_Manager
#         reporting_manager_object = self.employee_service.get_employee(reporting_manager_id)
#         reporting_manager_name = reporting_manager_object.Staff_FName + " " + reporting_manager_object.Staff_LName

#         # Original ISO 8601 date string
#         iso_date = date

#         # Convert to a datetime object in UTC
#         dt_utc = datetime.fromisoformat(iso_date[:-1])  # Remove the 'Z' for compatibility
#         dt_utc = dt_utc.replace(tzinfo=pytz.utc)  # Set timezone to UTC

#         # Convert to Singapore timezone
#         singapore_tz = pytz.timezone('Asia/Singapore')
#         dt_singapore = dt_utc.astimezone(singapore_tz)

#         # Format to dd-mm-yyyy
#         formatted_date = dt_singapore.strftime("%d-%m-%Y")

#         if shift == "FD":
#             shift = "Full Day"
        

#         message = f"""Subject: New WFH Request from {employee_name}

# Hi {reporting_manager_name},

#     This email is to inform you of a new work-from-home request submitted by {employee_name}.

#     Request Details:
#     - Date to WFH: {formatted_date}
#     - Shift: {shift}
#     - Reason: {reason}

#     Please review and respond accordingly.

# Thank you,
# WFH System"""
#         self.send_email("innocentstriker1@gmail.com", message)

    def send_email(self, to_email: str, message: str) -> None:
        import smtplib
        from getpass import getpass

        HOST = "smtp.gmail.com"
        PORT = 587
        FROM_EMAIL = "rotiprataspm1@gmail.com"
        PASSWORD = "salt noay zipe psuv"  # Use a more secure way to handle passwords

        smtp = smtplib.SMTP(HOST, PORT)

        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
        print(f"[*] Logging in: {status_code} {response}")

        smtp.sendmail(FROM_EMAIL, to_email, message)
        smtp.quit()
    


    # def alert_staff(self, staffID: str, startDate: str, endDate: str, actionType: str) -> None:
    def alert_staff(self, staffID: str, date: str, shift: str, actionType: str, approving_manager: str) -> None:

        import pytz

        employee_object = self.employee_service.get_employee(staffID)
        employee_name = employee_object.Staff_FName + " " + employee_object.Staff_LName
        
        if actionType == "approve":
            actionType = "approved"
        else:
            actionType = "rejected"

        # Original ISO 8601 date string
        iso_date = date

        # Convert to a datetime object in UTC
        dt_utc = datetime.fromisoformat(iso_date[:-1])  # Remove the 'Z' for compatibility
        dt_utc = dt_utc.replace(tzinfo=pytz.utc)  # Set timezone to UTC

        # Convert to Singapore timezone
        singapore_tz = pytz.timezone('Asia/Singapore')
        dt_singapore = dt_utc.astimezone(singapore_tz)

        # Format to dd-mm-yyyy
        formatted_date = dt_singapore.strftime("%d-%m-%Y")

        if shift == "FD":
            shift = "Full Day"
        

        message = f"""Subject: WFH Request {actionType}

Hi {employee_name},

    This email is to inform you that your WFH request for {formatted_date} for {shift} shift has been {actionType} by {approving_manager}.


Thank you,
WFH System"""
        self.send_email("innocentstriker1@gmail.com", message)

    def send_email(self, to_email: str, message: str) -> None:
        import smtplib
        from getpass import getpass

        HOST = "smtp.gmail.com"
        PORT = 587
        FROM_EMAIL = "rotiprataspm1@gmail.com"
        PASSWORD = "salt noay zipe psuv"  # Use a more secure way to handle passwords

        smtp = smtplib.SMTP(HOST, PORT)

        status_code, response = smtp.ehlo()
        print(f"[*] Echoing the server: {status_code} {response}")

        status_code, response = smtp.starttls()
        print(f"[*] Starting TLS connection: {status_code} {response}")

        status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
        print(f"[*] Logging in: {status_code} {response}")

        smtp.sendmail(FROM_EMAIL, to_email, message)
        smtp.quit()


    def get_wfh_request(self, request_id: str) -> WfhRequest:
        return self.wfh_request_repository.get_wfh_request(request_id)

    def get_all_wfh_requests(self) -> list[WfhRequest]:
        return self.wfh_request_repository.get_all_wfh_requests()
    
    def get_wfh_requests_by_staff_id(self, staff_id: str) -> list[WfhRequest]:
        return self.wfh_request_repository.get_wfh_requests_by_staff_id(staff_id)
    
    def get_wfh_requests_by_status(self, status: str) -> list[WfhRequest]:
        return self.wfh_request_repository.get_wfh_requests_by_status(status)
    
    def update_wfh_request(self, request_id: str, wfh_request: WfhRequest):
        self.wfh_request_repository.update_wfh_request(request_id, wfh_request)
    
    def delete_wfh_request(self, request_id: str):
        self.wfh_request_repository.delete_wfh_request(request_id)

    def get_schedules_and_employees_by_dept(self, dept: str, role: str) -> dict:
        return self.wfh_request_repository.get_schedules_and_employees_by_dept(dept, role)