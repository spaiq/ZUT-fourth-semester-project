from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Availability(models.Model):
    date = models.DateField()
    instructors = models.ManyToManyField(User, related_name="availabilities")

    def __str__(self):
        return str(self.date)


class Swimmer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Group(models.Model):
    level = models.CharField(max_length=100)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    swimmer = models.ManyToManyField(Swimmer, blank=True)

    def __str__(self):
        return (
            self.level
            + " "
            + self.instructor.first_name
            + " "
            + self.instructor.last_name
        )


class Lesson(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.start_date) + " " + str(self.end_date) + " " + self.group.level

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            if self.end_date <= self.start_date:
                raise ValidationError("End date must be after start date.")
        super().save(*args, **kwargs)


class Payment(models.Model):
    swimmer = models.ForeignKey(Swimmer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.swimmer) + " " + str(self.amount) + "PLN " + str(self.date)
