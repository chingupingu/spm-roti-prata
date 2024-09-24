from flask import jsonify, request
from .services.employee_service import EmployeeService

# instantiate services here
employee_service = EmployeeService()

# add routes here
def register_routes(app):
    @app.route("/employee", methods=["POST"])
    def create_employee():
        data = request.json
        doc_id = employee_service.create_employee(data["Staff_Fname"], 
                                                  data["Staff_LName"], 
                                                  data["Dept"], 
                                                  data["Position"], 
                                                  data["Country"], 
                                                  data["Email"], 
                                                  data["Reporting_Manager"], 
                                                  data["Role"]
                                                  )
        return jsonify({"doc_id": doc_id}), 201
    
    @app.route('/employee/<doc_id>', methods=['GET'])
    def get_employee(doc_id):
        employee = employee_service.get_employee(doc_id)
        if employee:
            return jsonify(employee.__dict__)
        return jsonify({'error': 'User not found'}), 404
    
    @app.route('/employee/<doc_id>', methods=['PUT'])
    def update_employee(doc_id):
        data = request.json
        employee = employee_service.get_employee(doc_id)
        if employee:
            employee.Staff_FName = data.get('Staff_FName', employee.Staff_FName)
            employee.Staff_LName = data.get('Staff_LName', employee.Staff_LName)
            employee.Dept = data.get('Dept', employee.Dept)
            employee.Position = data.get('Position', employee.Position)
            employee.Country = data.get('Country', employee.Country)
            employee.Email = data.get('Email', employee.Email)
            employee.Reporting_Manager = data.get('Reporting_Manager', employee.Reporting_Manager)
            employee.Role = data.get('Role', employee.Role)
            employee_service.update_employee(employee)
            return jsonify(employee.__dict__)
        return jsonify({'error': 'employee not found'}), 404

    @app.route('/employee/<doc_id>', methods=['DELETE'])
    def delete_employee(doc_id):
        employee_service.delete_employee(doc_id)
        return '', 204

    @app.route('/employee', methods=['GET'])
    def get_all_employees():
        employees = employee_service.get_all_employees()
        return jsonify([employee.__dict__ for employee in employees])