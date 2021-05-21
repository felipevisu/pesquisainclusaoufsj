from django.urls import path

from . import views

urlpatterns = [
    path('', views.IntroView.as_view(), name="intro"),
    path('<int:pk>/', views.SurveyView.as_view(), name="survey_form"),
    path('<int:pk>/finalizado/', views.FinalizedView.as_view(), name="finalized"),
    path('enviar/', views.SendView.as_view(), name="send"),
    path('restart/', views.RestartView.as_view(), name="restart"),
]
