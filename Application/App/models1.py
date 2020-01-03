from .models import Titles


class ModelController:

    def __init__(self):
        pass

    def get_model_object(self, model_object=None, params={}):
        try:
            object_value = model_object.objects.get(**params)
            return object_value

        except Exception as e:
            raise Exception(e)

    def get_field_value(self, model_object=None, field_name=None, params={}):
        try:
            object_field_value = model_object.objects.filter(**params)
            if len(object_field_value) != 1:
                raise Exception("Invalid or No value in table `{}`".format(model_object.__class__))

            return object_field_value[0].__dict__[field_name]

        except Exception as e:
            raise Exception(e)

    def promote_employee(self, new_designation=None, params={}):
        try:
            object_value = Titles.objects.get(**params)
            object_value.title = new_designation
            object_value.save()

            return new_designation

        except Exception as e:
            raise Exception(e)

    def update_data(self, model_object=None, params={}, check_condition=[]):
        try:
            object_value = model_object(**params)
            for x in check_condition:
                method = getattr(object_value, x)
                if not method():
                    raise Exception('Check condition for `{}` with condition `{}` Failed'.format(model_object.__class__, x))

            object_value.save()
            return object_value

        except Exception as e:
            raise Exception(e)