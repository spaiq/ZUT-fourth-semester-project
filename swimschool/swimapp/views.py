from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import generics, permissions, status
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .models import *
from .serializers import *
from .permissions import IsManager, IsInstructor, IsBookkeeper


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
        IsBookkeeper or IsManager or permissions.IsAdminUser,
    ]


class LessonCreateView(generics.CreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [
        permissions.IsAuthenticated,
        IsBookkeeper or IsManager or permissions.IsAdminUser,
    ]
