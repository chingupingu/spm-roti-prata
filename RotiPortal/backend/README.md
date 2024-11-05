- to run the app: python3 run.py OR python run.py

FLOW OF DATA:
- frontend should never interact directly with database; this is to decouple components of our webapp
- instead, the flow will be as such:
    1. user interacts with frontend
    2. frontend javascript handles the request by sending a HTTP request to an endpoint (flask route e.g. https://spm-roti-prata.onrender.com/employee/doc_id)
    3. this endpoint belongs to a function of a service in our backend (e.g. the above endpoint belongs to the get_employee() function
    of our employee_services.py)
    4. this service function calls a function in the associated repository (e.g. get_employee() in employee_service.py calls
    get_employee() in employee_repository.py)
    5. finally, the function in the repository will directly interact with our database to perform an action (in this example
    returning an Employee object if there is a matching doc_id)

EDITING:
- new collection:
    1. create a new class in models.py
    2. create a new repository
    3. create a new service
    4. configure new routes in routes.py
    ** don't forget to import and instantiate necessary classes !

- new service function:
    1. add the function in the respective service .py file
    2. configure new routes in routes.py

MISC INFO:
- user role 1: HR and senior mgmt
- user role 2: normal staff
- user role 3: manager and director

- delegation: only role 1 and 3 can be given delegation