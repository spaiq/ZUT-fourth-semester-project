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
    class Meta:
        model = User
        fields = "__all__"


class SwimmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swimmer
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()
    instructor_list = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(groups__name="Instructor"),
        write_only=True,
    )
    swimmer = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    def get_swimmer(self, obj):
        return [swimmer.__str__() for swimmer in obj.swimmer.all()]

    def get_instructor(self, obj):
        return obj.instructor.get_full_name()

    def create(self, validated_data):
        instructor = validated_data.pop("instructor_list", [])
        group = Group.objects.create(instructor=instructor, **validated_data)
        return group


class SingleGroupSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()
    swimmer = serializers.SerializerMethodField()
    swimmer_list = serializers.PrimaryKeyRelatedField(
        queryset=Swimmer.objects.all(), write_only=True
    )
    level = serializers.CharField(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"

    def get_swimmer(self, obj):
        return [swimmer.__str__() for swimmer in obj.swimmer.all()]

    def get_instructor(self, obj):
        return obj.instructor.get_full_name()


class CalendarSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(read_only=True, slug_field="level")
    instructor = serializers.SerializerMethodField()
    start_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    end_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Lesson
        fields = "__all__"

    def get_instructor(self, obj):
        return obj.instructor.get_full_name()


class LessonSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), write_only=True
    )

    class Meta:
        model = Lesson
        fields = "__all__"

    def validate_instructor(self, value):
        group = self.initial_data.get("group")
        start_date = self.initial_data.get("start_date")
        end_date = self.initial_data.get("end_date")

        # Retrieve instructors with availability on the specific day
        instructors = User.objects.filter(groups__name="Instructor")
        instructors = instructors.objects.filter(
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
    swimmer_details = serializers.StringRelatedField(
        read_only=True, source="swimmer.__str__"
    )
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Payment
        fields = "__all__"
