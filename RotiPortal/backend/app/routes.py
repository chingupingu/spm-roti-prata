from flask import jsonify, request
from .services.employee_service import EmployeeService
from .services.wfh_request_service import WfhRequestService
from .services.schedule_service import ScheduleService

# instantiate services here
employee_service = EmployeeService()
wfh_request_service = WfhRequestService()
schedule_service = ScheduleService()

# add routes here
def register_routes(app):
    ################################################################
    #                      EMPLOYEE                                #
    ################################################################
    @app.route("/employee", methods=["POST"])
    def create_employee():
        data = request.json
        staff_id = employee_service.create_employee(data["Staff_FName"], 
                                                  data["Staff_LName"], 
                                                  data["Dept"], 
                                                  data["Position"], 
                                                  data["Country"], 
                                                  data["Email"], 
                                                  data["Reporting_Manager"], 
                                                  data["Role"]
                                                  )
        return jsonify({"Staff_ID": staff_id}), 201
    
    @app.route('/employee/<staff_id>', methods=['GET'])
    def get_employee(staff_id):
        employee = employee_service.get_employee(staff_id)
        if employee:
            return jsonify(employee.__dict__)
        return jsonify({'error': 'User not found'}), 404
    
    @app.route('/employee/<staff_id>', methods=['PUT'])
    def update_employee(staff_id):
        data = request.json
        employee = employee_service.get_employee(staff_id)
        if employee:
            employee.Staff_FName = data.get('Staff_FName', employee.Staff_FName)
            employee.Staff_LName = data.get('Staff_LName', employee.Staff_LName)
            employee.Dept = data.get('Dept', employee.Dept)
            employee.Position = data.get('Position', employee.Position)
            employee.Country = data.get('Country', employee.Country)
            employee.Email = data.get('Email', employee.Email)
            employee.Reporting_Manager = data.get('Reporting_Manager', employee.Reporting_Manager)
            employee.Role = data.get('Role', employee.Role)
            employee_service.update_employee(staff_id, employee)
            return jsonify(employee.__dict__)
        return jsonify({'error': 'employee not found'}), 404

    @app.route('/employee/<staff_id>', methods=['DELETE'])
    def delete_employee(staff_id):
        employee_service.delete_employee(staff_id)
        return '', 204

    @app.route('/employee', methods=['GET'])
    def get_all_employees():
        employees = employee_service.get_all_employees()
        # return jsonify([employee.__dict__ for employee in employees])
        return jsonify(employees)

    @app.route('/employee/login', methods=['POST'])
    def check_email_exists():
        data = request.json
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        exists = employee_service.get_employee_by_email(email)
        return jsonify(exists)
    

    ################################################################
    #                      WFH REQUESTS                            #
    ################################################################
    @app.route("/wfh_request", methods=["POST"])
    def create_wfh_request():
        data = request.json
        # attachment_file = None

        # if data.get("attachment"):
        #     attachment_file = data.get("attachment")
        attachment_file = data.get("attachment")
        request_id = wfh_request_service.create_wfh_request(
                                                    data["staff_id"], 
                                                    data["date"], 
                                                    data["shift"], 
                                                    data["reason"], 
                                                    data.get("recurring", False), 
                                                    attachment_file,
                                                    data["status"]
                                                    )
        return jsonify({"request_id": request_id}), 201
    
    @app.route('/wfh_request/<request_id>', methods=['GET'])
    def get_wfh_request(request_id):
        wfh_request = wfh_request_service.get_wfh_request(request_id)
        if wfh_request:
            return jsonify(wfh_request.__dict__)
        return jsonify({'error': 'wfh_request not found'}), 404
    
    @app.route('/wfh_request', methods=['GET'])
    def get_all_wfh_requests():
        wfh_requests = wfh_request_service.get_all_wfh_requests()
        return jsonify(wfh_requests)
    
    @app.route('/wfh_request/staff/<staff_id>', methods=['GET'])
    def get_wfh_requests_by_staff_id(staff_id):
        wfh_requests = wfh_request_service.get_wfh_requests_by_staff_id(staff_id)
        return jsonify(wfh_requests)
    
    @app.route('/wfh_request/status/<status>', methods=['GET'])
    def get_wfh_requests_by_status(status):
        wfh_requests = wfh_request_service.get_wfh_requests_by_status(status)
        return jsonify(wfh_requests)

    @app.route('/wfh_request/<request_id>', methods=['PUT'])
    def update_wfh_request(request_id):
        data = request.json
        new_attachment = request.files.get('attachment')
        wfh_request = wfh_request_service.get_wfh_request(request_id)
        if wfh_request:
            wfh_request.staff_id = data.get('staff_id', wfh_request.staff_id)
            wfh_request.date = data.get('date', wfh_request.date)
            wfh_request.shift = data.get('shift', wfh_request.shift)
            wfh_request.reason = data.get('reason', wfh_request.reason)
            wfh_request.recurring = data.get('recurring', wfh_request.recurring)
            # wfh_request.attachment_url = data.get('attachment_url', wfh_request.attachment_url)
            wfh_request.status = data.get('status', wfh_request.status)

            if new_attachment:
                if wfh_request.attachment_url:
                    wfh_request_service.delete_attachment(wfh_request.attachment_url)
            
            # Upload new attachment and get new URL
                new_attachment_url = wfh_request_service.upload_attachment(new_attachment, request_id)
                wfh_request.attachment_url = new_attachment_url

            wfh_request_service.update_wfh_request(request_id, wfh_request)
            return jsonify(wfh_request.__dict__)
        return jsonify({'error': 'wfh_request not found'}), 404
    
    @app.route('/wfh_request/<request_id>', methods=['DELETE'])
    def delete_wfh_request(request_id):
        wfh_request_service.delete_wfh_request(request_id)
        return '', 204
    

    ################################################################
    #                   SCHEDULE REQUESTS                          #
    ################################################################
    @app.route("/schedule", methods=["POST"])
    def create_schedule():
        data = request.json
        doc_id = schedule_service.create_schedule(data["Staff_ID"], 
                                                  data["Date"], 
                                                  data["Duration"], 
                                                  data["Status"], 
                                                  data["Work_Arrangement"]
                                                  )
        return jsonify({"doc_id": doc_id}), 201
    
    @app.route('/schedule/<doc_id>', methods=['GET'])
    def get_schedule(doc_id):
        schedule = schedule_service.get_schedule(doc_id)
        if schedule:
            return jsonify(schedule.__dict__)
        return jsonify({'error': 'Schedule not found'}), 404
    
    @app.route('/schedule/<doc_id>', methods=['PUT'])
    def update_schedule(doc_id):
        data = request.json
        schedule = schedule_service.get_schedule(doc_id)
        if schedule:
            schedule.Staff_ID = data.get('Staff_ID', schedule.Staff_ID)
            schedule.Date = data.get('Date', schedule.Date)
            schedule.Duration = data.get('Duration', schedule.Duration)
            schedule.Status = data.get('Status', schedule.Status)
            schedule.Work_Arrangement = data.get('Work_Arrangement', schedule.Work_Arrangement)
            schedule_service.update_schedule(schedule)
            return jsonify(schedule.__dict__)
        return jsonify({'error': 'Schedule not found'}), 404

    @app.route('/schedule/<doc_id>', methods=['DELETE'])
    def delete_schedule(doc_id):
        schedule_service.delete_schedule(doc_id)
        return '', 204

    @app.route('/schedule', methods=['GET'])
    def get_all_schedules():
        schedules = schedule_service.get_all_schedules()
        return jsonify([schedule.__dict__ for schedule in schedules])
