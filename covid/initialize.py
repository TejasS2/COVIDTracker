import os
os.chdir("..")

import django
# In case that we need it later
# from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'covid.settings')
# This is for async, in case we will see it later (maybe) 
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import json
import http.client
from datetime import datetime
from countries.models import Country, Data

from asgiref.sync import sync_to_async

from django.conf import settings
conn = http.client.HTTPSConnection("covid-193.p.rapidapi.com")

api_key = settings.API_KEY
headers = {
    'X-RapidAPI-Key': api_key,
    'X-RapidAPI-Host': "covid-193.p.rapidapi.com"
}

conn.request("GET", "/countries", headers=headers)

res = conn.getresponse()
data = res.read()

countries = (data.decode("utf-8"))
countries_data = json.loads(countries)
country_list = countries_data.get('response', [])

async def fetch_countries():
    if not country_list:
        sys.exit(1)
    
    for country in country_list:
        country_obj, created = await sync_to_async(Country.objects.get_or_create)(name=country)

async def fetch_data(country, date):
    start_date = datetime.strptime(date, '%Y-%m-%d').date()
    formatted_date = start_date.strftime('%Y-%m-%d')
        
    conn.request("GET", f"/history?country={country}&day={formatted_date}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    dico_data = json.loads(data.decode('utf-8'))
    if not dico_data.get('response'):
        print(f"No data for {country} on {formatted_date}")
        sys.exit(1)
    # Parse the API response and save data to the database
    if 'response' in dico_data:
        for record in dico_data['response']:
            # Extract data from the record
            country_name = record['country']
            population = record['population']
            date = record['day']
            new_cases = int(record['cases']['new'].replace('+', '')) if record['cases']['new'] else 0
            total_cases = record['cases']['total'] if record['cases']['total'] else 0
            new_deaths = int(record['deaths']['new'].replace('+', '')) if record['deaths']['new'] else 0
            total_deaths = record['deaths']['total'] if record['deaths']['total'] else 0
            critical_cases = record['cases']['critical'] if record['cases']['critical'] else 0
            recovered_cases = record['cases']['recovered'] if record['cases']['recovered'] else 0
            cases_per_1M = int(record['cases']['1M_pop']) if record['cases']['1M_pop'] else 0
            total_tests = record['tests']['total'] if record['tests']['total'] else 0
            tests_per_1M = int(record['tests']['1M_pop']) if record['tests']['1M_pop'] else 0
            
            country_obj, created = await sync_to_async(Country.objects.get_or_create)(name=country_name)
            # Create or update the data object
            data_obj, created = await sync_to_async(Data.objects.update_or_create)(
                country=country_obj,
                date=datetime.strptime(date, '%Y-%m-%d').date(),
                defaults={
                    'new_infected': new_cases,
                    'total_infected': total_cases,
                    'new_deaths': new_deaths,
                    'total_deaths': total_deaths,
                    'critical': critical_cases,
                    'recovered': recovered_cases,
                    'cases_per_1M': cases_per_1M,
                    'total_tests': total_tests,
                    'test_per_1M': tests_per_1M,
                    'population': population,
                }
            )
            
            pass
    else:
        print(f"No data for {country} on {formatted_date}")

import asyncio
import sys
async def main():
    if len(sys.argv) == 1:
        await fetch_countries()
    elif len(sys.argv) == 3:
        country_name = sys.argv[1]
        date = sys.argv[2]
        await fetch_data(country_name, date)

if __name__ == "__main__":
    asyncio.run(main())
