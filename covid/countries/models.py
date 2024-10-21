from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Data(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='data')
    date = models.DateField()
    total_deaths = models.IntegerField()
    new_deaths = models.IntegerField()
    new_infected = models.IntegerField()
    total_infected = models.IntegerField()
    critical = models.IntegerField()
    recovered = models.IntegerField()
    cases_per_1M = models.IntegerField()
    total_tests = models.IntegerField()
    test_per_1M = models.IntegerField()
    population = models.IntegerField()

    class Meta:
        unique_together = ('country', 'date')

    def __str__(self):
        return f"{self.country.name} data for {self.date}"

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    notification = models.BooleanField(default=True)

    def __str__(self):
        return self.name