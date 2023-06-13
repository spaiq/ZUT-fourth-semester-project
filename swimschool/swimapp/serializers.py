from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
        label="Password",
        help_text="Password",
        min_length=8,
        max_length=128,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model = User
        fields = "__all__"


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = "__all__"


class InstructorSerializer(serializers.ModelSerializer):
    availability = AvailabilitySerializer()

    class Meta:
        model = Instructor
        fields = "__all__"


class SwimmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swimmer
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer()
    swimmer = SwimmerSerializer()

    class Meta:
        model = Group
        fields = "__all__"


class CalendarSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), write_only=True
    )
    swimmer = serializers.PrimaryKeyRelatedField(
        queryset=Swimmer.objects.all(), write_only=True
    )
    instructor = serializers.PrimaryKeyRelatedField(
        queryset=Instructor.objects.none(), write_only=True
    )

    class Meta:
        model = Calendar
        fields = "__all__"

    def validate_instructor(self, value):
        group = self.initial_data.get("group")
        start_date = self.initial_data.get("start_date")
        end_date = self.initial_data.get("end_date")

        # Retrieve instructors with availability on the specific day
        instructors = Instructor.objects.filter(
            availability__date__range=[start_date, end_date]
        ).distinct()

        if value not in instructors:
            raise serializers.ValidationError("Invalid instructor selection.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    swimmer = serializers.PrimaryKeyRelatedField(
        queryset=Swimmer.objects.all(),
        write_only=True,
    )
    swimmer_details = SwimmerSerializer(source="swimmer", read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"
