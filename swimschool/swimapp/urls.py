from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("calendar/", calendar, name="calendar"),
    path("calendar/endpoint/", CalendarView.as_view(), name="calendar-endpoint"),
    path("calendar/create/", LessonCreateView.as_view()),
    path("calendar/<int:pk>", LessonView.as_view()),
    path("contact/", contact, name="contact"),
    path("faq/", faq, name="faq"),
    path("instructors/", instructors, name="instructors"),
    path("bookkeeping/", BookkeepingView.as_view(), name="bookkeeping"),
    path("groups/", GroupView.as_view(), name="groups"),
    path("groups/<int:pk>", SingleGroupView.as_view()),
    path("manage-instructors/", InstructorView.as_view(), name="manage-instructors"),
    path(
        "manage-instructors/<int:pk>",
        SingleInstructorView.as_view(),
        name="manage-instructors",
    ),
    path("manage-bookkeepers/", BookkeeperView.as_view(), name="manage-bookkeepers"),
    path(
        "manage-bookkeepers/<int:pk>",
        SingleBookkeeperView.as_view(),
        name="manage-bookkeepers",
    ),
]
