from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics, permissions, status
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.decorators import login_required
from .models import *
from .serializers import *
from .permissions import IsManager, IsInstructor, IsBookkeeper
from django.utils.decorators import method_decorator
from django.contrib.auth import models
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


@throttle_classes([AnonRateThrottle, UserRateThrottle])
def index(request):
    return render(request, "index.html", {})


@throttle_classes([AnonRateThrottle, UserRateThrottle])
def about(request):
    return render(request, "about.html", {})


@throttle_classes([AnonRateThrottle, UserRateThrottle])
def faq(request):
    return render(request, "faq.html", {})


@throttle_classes([AnonRateThrottle, UserRateThrottle])
def contact(request):
    return render(request, "contact.html", {})


@throttle_classes([AnonRateThrottle, UserRateThrottle])
@login_required
def manage(request):
    return render(request, "manage.html", {})


@throttle_classes([AnonRateThrottle, UserRateThrottle])
def instructors(request):
    return render(request, "instructors.html", {})


@throttle_classes([AnonRateThrottle, UserRateThrottle])
def calendar(request):
    response = requests.get("http://127.0.0.1:8000/calendar/endpoint")
    data = response.json()
    lessons = data["results"]
    return render(request, "calendar.html", {"lessons": lessons})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("manage")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


class CalendarView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CalendarSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


@method_decorator(login_required, name="dispatch")
class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsInstructor | IsManager | permissions.IsAdminUser,
    ]


@method_decorator(login_required, name="dispatch")
class PaymentsView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsBookkeeper | IsManager | permissions.IsAdminUser,
    ]


@method_decorator(login_required, name="dispatch")
class SinglePaymentView(generics.RetrieveDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsBookkeeper | IsManager | permissions.IsAdminUser,
    ]


@method_decorator(login_required, name="dispatch")
class LessonView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CalendarSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsInstructor | IsManager | permissions.IsAdminUser,
    ]


@method_decorator(login_required, name="dispatch")
class GroupView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsInstructor | IsManager | permissions.IsAdminUser,
    ]

    def get_queryset(self):
        user = self.request.user
        group = models.Group.objects.filter(user=user).first()

        if group and group.name == "Manager":
            return Group.objects.all()

        return Group.objects.filter(instructor_id=self.request.user)


@method_decorator(login_required, name="dispatch")
class SingleGroupView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = SingleGroupSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsInstructor | IsManager | permissions.IsAdminUser,
    ]

    def perform_update(self, serializer):
        swimmer = serializer.validated_data.get("swimmer_list", [])
        existing_swimmers = serializer.instance.swimmer.all()

        if swimmer not in existing_swimmers:
            serializer.instance.swimmer.add(swimmer)
        else:
            serializer.instance.swimmer.remove(swimmer)

        serializer.save()

    def perform_destroy(self, instance):
        instance.swimmer.clear()
        instance.delete()


@method_decorator(login_required, name="dispatch")
class InstructorView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="Instructor")
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsManager | permissions.IsAdminUser,
    ]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.groups.add(Group.objects.get(name="Instructor"))
        user.save()


@method_decorator(login_required, name="dispatch")
class SingleInstructorView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name="Instructor")
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsManager | permissions.IsAdminUser,
    ]


@method_decorator(login_required, name="dispatch")
class BookkeeperView(generics.ListCreateAPIView):
    queryset = User.objects.filter(groups__name="Bookkeeper")
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsManager | permissions.IsAdminUser,
    ]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.groups.add(Group.objects.get(name="Bookkeeper"))
        user.save()


@method_decorator(login_required, name="dispatch")
class SingleBookkeeperView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name="Bookkeeper")
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsManager | permissions.IsAdminUser,
    ]
