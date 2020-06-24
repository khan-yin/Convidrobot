from django.urls import path
from . import views
app_name='robot'

urlpatterns = [
    path('getphoto/', views.getphoto,name='getphoto'),
    path('test/', views.Test.as_view()),
    path('dataadd/',views.DATAADD.as_view()),
    path('datachart/',views.DATACHART.as_view()),
    path('datamap/',views.DATAMAP.as_view()),
    path('getcomments/',views.COMMENTS.as_view()),
    path('getanswer/',views.getanswer,name='getanswer'),
    path('addstar/',views.addstar,name='addstar'),
    path('deletestar/',views.deletestar,name='deletestar')
]