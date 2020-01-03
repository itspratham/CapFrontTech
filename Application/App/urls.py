from . import views
from django.urls import path, re_path

urlpatterns = {

    path('employee_hire', views.EmployeeHire.as_view()),
    re_path(r'eligible_for_hike/(?P<emp_no>[0-9]+)$', views.EligibleForHike.as_view())
}


