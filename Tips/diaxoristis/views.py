from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
#from diaxoristis.models import Employee,Posto,Tip
from diaxoristis.forms import (EmployeeForm,PostoForm,TipForm,StepOneEmployeeForm,
                               StepTwoEmployeeForm)
from django.urls import reverse_lazy
from django.views.generic import(TemplateView,ListView,
                                 DetailView,CreateView,UpdateView,
                                 DeleteView,FormView)
from . import models
from . import tipsLib
from . import app_settings

# Create your views here.

class AboutView(TemplateView):
    template_name = 'diaxoristis/about.html'


class IndexView(TemplateView):
    template_name = 'diaxoristis/index.html'

class StepOneView(FormView):
    template_name = 'diaxoristis/step_one.html'
    form_class = StepOneEmployeeForm
    success_url=reverse_lazy('diaxoristis:step_two')



    def form_valid(self, form_class):


        self.get_data(form_class.cleaned_data)
        return super(StepOneView, self).form_valid(form_class)

    def get_data(self, valid_data):
        app_settings.MyPosto = []
        app_settings.MyEmployees = []
        app_settings.Dynamic_Fields=[]
        # Αποθηεκεύουμε το πόστο
        app_settings.MyPosto = valid_data['posta']
        employees =valid_data['employees']
        #πέρνουμε τα object υπαλλήλων και τα αποθηκεύουμε σε λίστα
        for i in employees:
            emp = models.Employee.objects.get(name=i)
            app_settings.MyEmployees.append(emp)



class StepTwoView(FormView):
    template_name = 'diaxoristis/step_two.html'
    form_class=None
    form_class = StepTwoEmployeeForm
    success_url=reverse_lazy('diaxoristis:step_three')




    def form_valid(self, form_class):
        self.execute(form_class.cleaned_data)
        return super(StepTwoView, self).form_valid(form_class)

    def execute(self, valid_data):
        app_settings.Diaxoristis = None
        data = valid_data
        money = data['money']
        date_from = data['date_from']
        date_until = data["date_until"]
        employee_Tip_object = []

        for i in app_settings.MyEmployees:
            days = data[i.name]
            ypallilos = tipsLib.Ypallilos(i.name,i.parts,merokamata= days)
            employee_Tip_object.append(ypallilos)

        posto_Tip_Object = tipsLib.Posto(app_settings.MyPosto)
        tips_Tip_Object = tipsLib.Tips(money,posto_Tip_Object,date_in=date_from,date_out=date_until)
        diaxoristis_Tip_Object = tipsLib.Diaxoristis(employee_Tip_object,tips_Tip_Object)
        app_settings.Diaxoristis = diaxoristis_Tip_Object
        app_settings.Result_Tips = app_settings.Diaxoristis.result()


def StepThreeView(request):
    template_name = 'diaxoristis/step_three.html'
    context ={}
    context['result'] = app_settings.Result_Tips

    def save_Tip():

        posto = models.Posto.objects.get(name=app_settings.Result_Tips["posto"])
        p = models.Tip.objects.create(posto= posto,
                                start_date=app_settings.Result_Tips["date_from"],
                                end_date=app_settings.Result_Tips["date_until"],
                                money=app_settings.Result_Tips["money"])

    if request.GET.get('submit'):

        save_Tip()

    return render(request,template_name,{"context":context})



#class StepThreeView(TemplateView):
#    template_name = 'diaxoristis/step_three.html'
#
#
#    def get_context_data(self, **kwargs):
#        context = super(StepThreeView, self).get_context_data(**kwargs)
#        context['result'] = app_settings.Result_Tips
#
#
#        return context
#
#    def save_Tip(self):
#        p = Person.objects.Tip(posto=app_settings.Result_Tips["posto"],
#                                start_date=app_settings.Result_Tips["date_from"],
#                                end_date=app_settings.Result_Tips["date_until"],
#                                money=app_settings.Result_Tips["money"])
#
#
#    def dispatch(self, request, *args, **kwargs):
#        for key in request.GET:
#            print(key)
#            value = request.GET[key]
#            print(value)
#        return super(StepThreeView, self).dispatch(request, *args, **kwargs)
    #def post(self, request):
        #submitbutton= self.request.POST
        #print(self.request.POST.post(''))
        #if submitbutton:
            #print("apothikeytike")
        #self.save_Tip()
class SavedView(TemplateView):
    template_name = 'diaxoristis/saved.html'

class EmployeeListView(ListView):
    model = models.Employee
    context_object_name = 'employees'

    def get_queryset(self):
        return models.Employee.objects.order_by('name')

class EmployeeDetailView(DetailView):
    context_object_name = 'employees_detail'
    model = models.Employee
    template_name = 'diaxoristis/employee_detail.html'

class EmployeeCreateView(CreateView):
    fields = ('name','parts')
    model = models.Employee
    success_url = reverse_lazy("diaxoristis:employee_list")

class EmployeeUpdateView(UpdateView):
    fields = ('name','parts')
    model = models.Employee
    success_url = reverse_lazy("diaxoristis:employee_list")

class EmployeeDeleteView(DeleteView):
    model = models.Employee
    success_url = reverse_lazy("diaxoristis:employee_list")

class PostoListView(ListView):
    context_object_name = 'posta'
    model = models.Posto

    def get_queryset(self):
        return models.Posto.objects.order_by('name')

class PostoDetailView(DetailView):
    context_object_name = 'posto_detail'
    model = models.Posto
    template_name = 'diaxoristis/posto_detail.html'

class PostoCreateView(CreateView):
    fields = ('name',)
    model = models.Posto
    success_url = reverse_lazy("diaxoristis:posto_list")

class PostoUpdateView(UpdateView):
    fields = ('name',)
    model = models.Posto
    success_url = reverse_lazy("diaxoristis:posto_list")

class PostoDeleteView(DeleteView):
    model = models.Posto
    success_url = reverse_lazy("diaxoristis:posto_list")


class TipListView(ListView):
    context_object_name = 'tips'
    model = models.Tip

class TipDetailView(DetailView):
    context_object_name = 'tips_detail'
    model = models.Tip
    template_name = 'diaxoristis/tip_detail.html'

class TipDeleteView(DeleteView):
    model = models.Tip
    success_url = reverse_lazy("diaxoristis:tip_list")
