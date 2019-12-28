from django import forms
from diaxoristis.models import Posto,Employee,Tip
from . import app_settings


class EmployeeForm(forms.Form):

    class Meta():
        model = Employee
        fields = ('name','parts')
        labels = {
            "name":"Όνομα",
            "parts":"Μέρη"
            }

class PostoForm(forms.Form):

    class Meta():
        model = Posto
        fields = ("name",)
        labels = {
            "name":"Όνομα"
        }


class TipForm(forms.Form):

    class Meta():
        model = Tip
        fields = ('posto','money','start_date','end_date')

class StepOneEmployeeForm(forms.Form):

    employees = forms.ModelMultipleChoiceField(
        queryset = Employee.objects.all(), # or .filter(…) if you want only some articles to show up
        widget  = forms.CheckboxSelectMultiple,label = "Διάλεξε Υπαλλήλους:"
    )

    posta = forms.ModelChoiceField ( queryset = Posto.objects.all(), widget= forms.Select,label = "Διάλεξε πόστο:")


class StepTwoEmployeeForm(forms.Form):
    money = forms.FloatField(label = "Χρήματα:")
    date_from=forms.DateField(input_formats = app_settings.DATE_INPUT_FORMATS,label = "Από:")
    date_until=forms.DateField(input_formats = app_settings.DATE_INPUT_FORMATS,label = "Μέχρι:")


    def __init__(self, *args, **kwargs):
        extra=app_settings.MyEmployees



        super(StepTwoEmployeeForm,self).__init__(*args, **kwargs)


        if len(extra) !=0 :

            for i in extra:

                for i in extra:
                    self.fields[i.name] = forms.IntegerField(label = i.name)
                    app_settings.Dynamic_Fields.append(i.name)
