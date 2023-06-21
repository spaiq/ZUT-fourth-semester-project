from django.urls import path
from .views import *
urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("calendar/", calendar, name="calendar"),
    path("calendar/endpoint/", CalendarView.as_view(), name="calendar-endpoint"),
    path("calendar/create/", LessonCreateView.as_view()),
    path("manage/calendar/", manage_calendar, name="calendar"),
    path("manage/calendar/<int:pk>", LessonView.as_view()),
    path("groups/", GroupView.as_view(), name="groups"),
    path("groups/add", AddGroupView.as_view(), name="add_manage_groups"),
    path("manage/groups/", manage_groups, name="manage_groups"),
    path("manage/groups/<int:pk>", SingleGroupView.as_view()),
    path("contact/", contact, name="contact"),
    path("manage/", manage, name="manage"),
    path("faq/", faq, name="faq"),
    path("instructors/", instructors, name="instructors"),
    path("payments/", PaymentsView.as_view(), name="payments"),
    path("payments/<int:pk>", SinglePaymentView.as_view(), name="payments"),

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
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", logout_view, name="logout"),
]

