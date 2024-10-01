from flask import jsonify, request
from .services.employee_service import EmployeeService

# instantiate services here
employee_service = EmployeeService()

# add routes here
def register_routes(app):
    @app.route("/employee", methods=["POST"])
    def create_employee():
        data = request.json
        doc_id = employee_service.create_employee(data["Staff_FName"], 
                                                  data["Staff_LName"], 
                                                  data["Dept"], 
                                                  data["Position"], 
                                                  data["Country"], 
                                                  data["Email"], 
                                                  data["Reporting_Manager"], 
                                                  data["Role"]
                                                  )
        return jsonify({"Staff_ID": doc_id}), 201
    
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