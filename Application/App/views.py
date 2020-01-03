from django.shortcuts import render
from rest_framework.views import APIView
from django.http.response import HttpResponse
import json
import datetime
from .models import Employees, DepartmentEmployee, Salary, Titles, Departments
from .models1 import ModelController

# Create your views here.


class EmployeeHire(APIView):

    def get(self, request):
        return HttpResponse(json.dumps({"success": False, "error": "Method not Allowed"}), content_type='application/json')

    def post(self, request):
        try:
            L = 10000
            title_salary = {
                "Staff": 3 * L,
                "Senior staff": 5 * L,
                "Assistant Engineer": 7 * L,
                "Engineer": 9 * L,
                "Senior Engineer": 12 * L,
                "Technique Lead": 20 * L,
                "Manager": 30 * L
            }

            requested_data = json.loads(request.data["data"])
            dob = datetime.datetime.strptime(requested_data["birth_date"], "%Y-%m-%d").date()
            emp_no = requested_data["employee_id"]
            fname = requested_data["first_name"]
            lname = requested_data["last_name"]
            gender = requested_data["gender"]
            h_date = datetime.datetime.strptime(requested_data["hire_date"], "%Y-%m-%d").date()
            salary_from_date = datetime.datetime.strptime(requested_data["salary_from_date"], "%Y-%m-%d").date()
            salary_to_date = datetime.datetime.strptime(requested_data["salary_to_date"], "%Y-%m-%d").date()
            dept = requested_data["department"]
            title = requested_data["title"]

            model_controller = ModelController()
            dept_obj = model_controller.get_model_object(model_object=Departments,
                                                         params={'dept_name': dept})

            emp_obj = model_controller.update_data(model_object=Employees,
                                                    params={'emp_no': emp_no,
                                                            'birth_date': dob,
                                                            'first_name': fname,
                                                            'last_name': lname,
                                                            'gender': gender,
                                                            'hire_date': h_date},
                                                   check_condition=['check_age']
                                                   )

            dept_emp = model_controller.update_data(model_object=DepartmentEmployee,
                                                    params={'emp_no': emp_obj,
                                                            'dept_no': dept_obj,
                                                            'from_date': salary_from_date,
                                                            'to_date': salary_to_date})

            title_obj = model_controller.update_data(model_object=Titles,
                                                     params={'emp_no': emp_obj,
                                                             'title': title,
                                                             'from_date': salary_from_date,
                                                             'to_date': salary_to_date})

            sal_obj = model_controller.update_data(model_object=Salary,
                                                   params={'emp_no': emp_obj,
                                                           'salary': title_salary[title],
                                                           'from_date': salary_from_date,
                                                           'to_date': salary_to_date})

            return HttpResponse(json.dumps({"success": True}), content_type="application/json")

        except KeyError as e:
            return HttpResponse(json.dumps({"success": True, "error": "Missing `{}` from Requested Data".format(e)}), content_type='application/json')

        except Exception as e:
            return HttpResponse(json.dumps({"success":True, "error": "{}".format(e)}), content_type='application/json')


class EligibleForHike(APIView):

    def post(self, request):
        return HttpResponse(json.dumps({"success": False, "error": "Method not Allowed"}),
                            content_type='application/json')

    def get(self, request, emp_no=None):
        try:

            if emp_no is None:
                raise Exception("Invalid Request")

            model_controller = ModelController()

            emp_obj = model_controller.get_model_object(model_object=Employees,
                                                        params={'emp_no': emp_no})
            not_dept = ["Customer Service", "Development", "Finance", "Human Resources", "Human Resources", "Sales"]
            not_title = ["Senior Engineer", "Staff", "Engineer", "Senior Staff", "Assistant Engineer", "Technique Leader"]

            dept_id = model_controller.get_field_value(model_object=DepartmentEmployee,
                                                       field_name='dept_no_id',
                                                       params={'emp_no': emp_obj})

            dept = model_controller.get_field_value(model_object=Departments,
                                                    field_name='dept_name',
                                                    params={'dept_no': dept_id})

            if dept not in not_dept:
                return HttpResponse(json.dumps({"hike": False}), content_type="application/json")

            title = model_controller.get_field_value(model_object=Titles,
                                                     field_name='title',
                                                     params={'emp_no': emp_obj})

            if title not in not_title:
                return HttpResponse(json.dumps({"hike": False}), content_type="application/json")

            hire_date = emp_obj.hire_date
            dob = emp_obj.birth_date
            gender = emp_obj.gender
            if datetime.date.today() - hire_date <= datetime.timedelta(365) or datetime.date.today() - dob <= datetime.timedelta(7300) :
                return HttpResponse(json.dumps({"hike": False}), content_type="application/json")

            if gender == 'M' and title == "Technique Leader":
                return HttpResponse(json.dumps({"hike": False}), content_type="application/json")

            promotion = ["Staff", "Senior staff", "Assistant Engineer", "Engineer", "Senior Engineer", "Technique Leader",
                         "Manager"]

            promoted_title = model_controller.promote_employee(new_designation=promotion[promotion.index(title) + 1],
                                                               params={'emp_no': emp_obj})

            return HttpResponse(json.dumps({"hike": True, "designation": promoted_title}), content_type="application/json")

        except KeyError as e:
            return HttpResponse(json.dumps({"success": True, "error": "Missing `{}` from Data".format(e)}),
                                content_type='application/json')

        except Exception as e:
            return HttpResponse(json.dumps({"success": True, "error": "{}".format(e)}), content_type='application/json')

