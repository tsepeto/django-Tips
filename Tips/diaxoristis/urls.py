from django.urls  import path,re_path
from diaxoristis import views

app_name = 'diaxoristis'

urlpatterns = [
    path("",views.IndexView.as_view(),name = 'index'),
    path("about/",views.AboutView.as_view(),name = 'about'),

    path("list_employee/",views.EmployeeListView.as_view(),name = 'employee_list'),
    path('list_employee/<int:pk>/',views.EmployeeDetailView.as_view(),name = 'employee_detail'),
    path("create_employee/",views.EmployeeCreateView.as_view(),name = "employee_create"),
    re_path('update_employee/(?P<pk>\d+)/',views.EmployeeUpdateView.as_view(),name = 'employee_update'),
    re_path('delete_employee/(?P<pk>\d+)/',views.EmployeeDeleteView.as_view(),name = 'employee_delete'),

    path("list_posto/",views.PostoListView.as_view(),name = 'posto_list'),
    path('list_posto/<int:pk>/',views.PostoDetailView.as_view(),name = 'posto_detail'),
    path("create_posto/",views.PostoCreateView.as_view(),name = "posto_create"),
    re_path('update_posto/(?P<pk>\d+)/',views.PostoUpdateView.as_view(),name = 'posto_update'),
    re_path('delete_posto/(?P<pk>\d+)/',views.PostoDeleteView.as_view(),name = 'posto_delete'),

    path("list_tip/",views.TipListView.as_view(),name = 'tip_list'),
    path('list_tip/<int:pk>/',views.TipDetailView.as_view(),name = 'tip_detail'),
    re_path('delete_tip/(?P<pk>\d+)/',views.TipDeleteView.as_view(),name = 'tip_delete'),

    path("step_one/",views.StepOneView.as_view(),name = 'step_one'),
    path("step_two/",views.StepTwoView.as_view(),name = 'step_two'),
    path("step_three/",views.StepThreeView,name = 'step_three'),

    path("step_three/saved/",views.SavedView.as_view(),name = "saved"),
]
