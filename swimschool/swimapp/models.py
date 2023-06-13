from django.db import models


class Availability(models.Model):
    date = models.DateField()
    availability = models.BooleanField(default=True)

    def __str__(self):
        return str(self.date)


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    availability = models.ManyToManyField(Availability)

    def __str__(self):
        return self.first_name + " " + self.last_name


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
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    swimmer = models.ManyToManyField(Swimmer)

    def __str__(self):
        return (
            self.level
            + " "
            + self.instructor.first_name
            + " "
            + self.instructor.last_name
        )


class Calendar(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.start_date) + " " + str(self.end_date) + " " + self.group.level


class Payment(models.Model):
    swimmer = models.ForeignKey(Swimmer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.swimmer) + " " + str(self.amount) + "PLN " + str(self.date)
