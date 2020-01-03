from django.db import models

# Create your models here.
from django.db import models
import datetime
# Create your models here.


class Employees(models.Model):

    class Meta:
        db_table = 'employees'

    genders_tuple = (('M', 'Male'), ('F', 'Female'))

    emp_no = models.IntegerField(primary_key=True)
    birth_date = models.DateField()
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=16)
    gender = models.CharField(max_length=1, choices=genders_tuple)
    hire_date = models.DateField()

    def check_age(self):
        diff = self.birth_date - datetime.date.today()
        if not (diff >= datetime.timedelta(6570) or diff <= datetime.timedelta(21900)):
            return False
        return True


class Departments(models.Model):

    class Meta:
        db_table = 'departments'

    dept_no = models.CharField(max_length=4, primary_key=True)
    dept_name = models.CharField(max_length=40, unique=True)


class DepartmentEmployee(models.Model):

    class Meta:
        db_table = 'dept_emp'
        unique_together = (('emp_no', 'dept_no'), )

    emp_no = models.ForeignKey(Employees, on_delete=models.CASCADE)
    dept_no = models.ForeignKey(Departments, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()


class Titles(models.Model):

    class Meta:
        db_table = 'titles'
        unique_together = (('emp_no', 'title', 'from_date'),)

    emp_no = models.ForeignKey(Employees, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField(null=True)


class Salary(models.Model):

    class Meta:
        db_table = 'salaries'
        unique_together = (('emp_no', 'from_date'),)

    emp_no = models.ForeignKey(Employees, on_delete=models.CASCADE)
    salary = models.IntegerField()
    from_date = models.DateField()
    to_date = models.DateField()
