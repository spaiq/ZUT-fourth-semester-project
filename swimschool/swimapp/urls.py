from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("calendar/", CalendarView.as_view(), name="calendar"),
    path("calendar/add", LessonCreateView.as_view()),
    path("contact/", contact, name="contact"),
    path("faq/", faq, name="faq"),
    path("instructors/", instructors, name="instructors"),
    path("bookkeeping/", BookkeepingView.as_view(), name="bookkeeping"),
]
