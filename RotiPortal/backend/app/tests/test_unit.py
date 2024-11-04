import json
import unittest
from unittest.mock import patch, Mock
from app import create_app
import os
import base64
from dotenv import load_dotenv, find_dotenv

class MockEmployee:
    def __init__(self, staff_id, first_name, last_name, dept, position):
        self.Staff_ID = staff_id
        self.Staff_FName = first_name
        self.Staff_LName = last_name
        self.Dept = dept
        self.Position = position

class MockWfhRequest:
    def __init__(self, request_id, staff_id, date, shift, status):
        self.request_id = request_id
        self.staff_id = staff_id
        self.date = date
        self.shift = shift
        self.status = status

class TestRoutes(unittest.TestCase):
    def setUp(self):
        # self.app = create_app()
        # self.client = self.app.test_client()
        # self.app.testing = True
        load_dotenv(find_dotenv())
        encoded_key = os.getenv('SERVICE_ACCOUNT_KEY')
        SERVICE_ACCOUNT_JSON = json.loads(base64.b64decode(encoded_key).decode('utf-8'))
        self.app = create_app(SERVICE_ACCOUNT_JSON)
        self.client = self.app.test_client()
        self.app.testing = True

    @patch('app.services.employee_service.EmployeeService.create_employee')
    def test_create_employee(self, mock_create_employee):
        # Mock the response from employee_service.create_employee
        mock_create_employee.return_value = "EMP123"
        
        # Test the POST request to create an employee
        response = self.client.post('/employee', json={
            "Staff_FName": "John",
            "Staff_LName": "Doe",
            "Dept": "Engineering",
            "Position": "Developer",
            "Country": "USA",
            "Email": "john.doe@example.com",
            "Reporting_Manager": "Manager1",
            "Role": "Employee"
        })
        
        # Assert status code and response data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"Staff_ID": "EMP123"})

    @patch('app.services.employee_service.EmployeeService.get_employee')
    def test_get_employee(self, mock_get_employee):
        # Create and return a mock employee object
        mock_employee = MockEmployee(
            staff_id="EMP123",
            first_name="John",
            last_name="Doe",
            dept="Engineering",
            position="Developer"
        )
        mock_get_employee.return_value = mock_employee

        # Test the GET request for a specific employee
        response = self.client.get('/employee/EMP123')

        # Assert status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "Staff_ID": "EMP123",
            "Staff_FName": "John",
            "Staff_LName": "Doe",
            "Dept": "Engineering",
            "Position": "Developer"
        })

    @patch('app.services.employee_service.EmployeeService.get_employee')
    def test_get_employee_not_found(self, mock_get_employee):
        # Mock that the employee is not found
        mock_get_employee.return_value = None
        
        # Test the GET request for a non-existing employee
        response = self.client.get('/employee/EMP999')
        
        # Assert status code and error message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "User not found"})

    @patch('app.services.employee_service.EmployeeService.get_all_employees')
    def test_get_all_employees(self, mock_get_all_employees):
        # Mock the employees returned by the service
        mock_get_all_employees.return_value = [
            {"Staff_ID": "EMP123", "Staff_FName": "John", "Dept": "Engineering"},
            {"Staff_ID": "EMP124", "Staff_FName": "Jane", "Dept": "Sales"}
        ]

        # Test the GET request to retrieve all employees
        response = self.client.get('/employee')
        
        # Assert status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {"Staff_ID": "EMP123", "Staff_FName": "John", "Dept": "Engineering"},
            {"Staff_ID": "EMP124", "Staff_FName": "Jane", "Dept": "Sales"}
        ])

    @patch('app.services.employee_service.EmployeeService.delete_employee')
    def test_delete_employee(self, mock_delete_employee):
        # Mock successful deletion
        mock_delete_employee.return_value = None
        
        # Test the DELETE request to delete an employee
        response = self.client.delete('/employee/EMP123')
        
        # Assert status code (204 No Content)
        self.assertEqual(response.status_code, 204)

    @patch('app.services.wfh_request_service.WfhRequestService.validate_wfh_request')
    def test_validate_wfh_request(self, mock_validate_wfh_request):
        # Mock the validation result
        mock_validate_wfh_request.return_value = (True, "WFH request is valid.")
        
        # Test the POST request to validate a WFH request
        response = self.client.post('/wfh_request/validate', json={
            "staff_id": "EMP123",
            "date": "2023-10-18"
        })
        
        # Assert status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"valid": True, "message": "WFH request is valid."})

    @patch('app.services.wfh_request_service.WfhRequestService.get_wfh_request')
    def test_get_wfh_request(self, mock_get_wfh_request):
        # Return a mock WFH request object
        mock_wfh_request = MockWfhRequest(
            request_id="REQ123",
            staff_id="EMP123",
            date="2023-10-18",
            shift="morning",
            status="pending"
        )
        mock_get_wfh_request.return_value = mock_wfh_request

        # Test the GET request for a specific WFH request
        response = self.client.get('/wfh_request/REQ123')

        # Assert status code and response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "request_id": "REQ123",
            "staff_id": "EMP123",
            "date": "2023-10-18",
            "shift": "morning",
            "status": "pending"
        })

    @patch('app.services.wfh_request_service.WfhRequestService.get_wfh_request')
    def test_get_wfh_request_not_found(self, mock_get_wfh_request):
        # Mock that the WFH request is not found
        mock_get_wfh_request.return_value = None
        
        # Test the GET request for a non-existing WFH request
        response = self.client.get('/wfh_request/REQ999')
        
        # Assert status code and error message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "wfh_request not found"})
