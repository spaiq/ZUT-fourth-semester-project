from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics, permissions, status
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import *
from .serializers import *
from .permissions import IsManager, IsInstructor, IsBookkeeper
from django.contrib.auth import models


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
def instructors(request):
    return render(request, "instructors.html", {})


class CalendarView(generics.ListAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]


class BookkeepingView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsBookkeeper | IsManager | permissions.IsAdminUser,
    ]


class LessonView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsInstructor | IsManager | permissions.IsAdminUser,
    ]


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

        return Group.objects.filter(user=self.request.user)


class SingleGroupView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsInstructor | IsManager | permissions.IsAdminUser,
    ]


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


class SingleInstructorView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name="Instructor")
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsManager | permissions.IsAdminUser,
    ]


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


class SingleBookkeeperView(generics.DestroyAPIView):
    queryset = User.objects.filter(groups__name="Bookkeeper")
    serializer_class = UserSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsManager | permissions.IsAdminUser,
    ]
