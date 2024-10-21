from .models import Data, User
from django.core.mail import send_mail
import requests


def create_daily_stats_email(country_id):
    try:
        latest_data = Data.objects.filter(country_id=country_id).latest('date')
        email_content = f"COVID-19 Update for {latest_data.country.name} on {latest_data.date}:\n"
        email_content += f"Total Deaths: {latest_data.total_deaths}\n"
        email_content += f"New Deaths: {latest_data.new_deaths}\n"
        email_content += f"New Infected: {latest_data.new_infected}\n"
        email_content += f"Total Infected: {latest_data.total_infected}\n"
        email_content += f"Critical Cases: {latest_data.critical}\n"
        email_content += f"Recovered Cases: {latest_data.recovered}\n"
        email_content += f"Cases per 1M: {latest_data.cases_per_1M}\n"
        email_content += f"Total Tests: {latest_data.total_tests}\n"
        email_content += f"Tests per 1M: {latest_data.test_per_1M}\n"
        return email_content
    except Data.DoesNotExist:
        return "No data available for the latest date."

def send_daily_notifications():
    for user in User.objects.filter(notification=True).select_related('country'):
        email_content = create_daily_stats_email(user.country_id)
        send_mail(
            'Daily COVID-19 Stats',
            f"Hi {user.name},\n{email_content}",
            'covidalert2024@gmail.com',
            [user.email],
            fail_silently=False,
        )
