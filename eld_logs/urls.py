from django.urls import path



from .views import generate_eld_log

app_name = "eld_logs"

urlpatterns = [
    path(
        "generate/<uuid:pk>/",
        generate_eld_log,
        name="generate-eld-log",
    ),
    



]