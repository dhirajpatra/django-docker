from django.urls import include, path
from rest_framework import routers
from task_manager import views

router = routers.DefaultRouter()
router.register(r'register_user', views.UserSignUpViewSet)
router.register(r'login_user', views.UserLoginViewset)
router.register(r'tasks', views.EmployeeTaskViewset)

urlpatterns = [
    path('', include(router.urls)),
    ]
