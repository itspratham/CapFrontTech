# CapFrontTech
Assignment Problem

Requisite

django==3.x

djangorestframework==3.9.0

Project contains two APIs as,

127.0.0.1:8000/employee/employee_hire
It is POST API and used to insert a new Employee Data. Requested data must be in the format as,

data:{"birth_date":"YYYY-MM-DD","employee_id":2,"first_name":"Manoj","last_name":"Kumar","gender":"M","hire_date":"2015-06-07","salary_from_date":"2015-06-07","salary_to_date":"2015-12-07","department":"Development","title":"Assistant Engineer"}

as sent from Postman.

Second api is,

127.0.0.1:8000/employee/eligible_for_hike/<employee_id>
It is GET API and used to check and update hike for eligible employee.

Example, 127.0.0.1:8000/employee/eligible_for_hike/2

Project is based on WSGI. To run the server please run command,

python manage.py runserver
