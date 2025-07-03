# from django.urls import path
# from . import views

# app_name='invoice'

# urlpatterns = [
#     path('',views.home,name="home"),
# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FactureViewSet,home,FileUploadView,IdentiferView,DashView

router = DefaultRouter()
router.register(r'factures', FactureViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload/', FileUploadView.as_view()),
    path('api/identcompte/', IdentiferView.as_view()),
    path('api/dashbord/', DashView.as_view()),
    path('',home,name="home"),
]
