import os
import requests
import re

# Available airlines and payment providers
airline_apis = {}
payment_provider_apis = {}

# Sort by cheapest


def sort_by_cheapest(flights):
    return sorted(flights, key=lambda flight: flight['price'])

# Validate input


email_regex = r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'
# Date in format dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy
date_regex = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'
# 16-digit card number
card_regex = r'^(\d{4}[-\s]?){3}\d{4}$'
# Only 3 digits
cvv_regex = r'^\d{3}$'
# Only uk numbers are accepted
phone_num_regex = r'^(\+44|0)?[\s]?\d{1,5}[\s]?\d{1,5}[\s]?\d{1,5}$'
# 3 uppercase letters followed by 4 digits
booking_ref_regex = r'^[A-Z]{3}\d{4}$'


def validate_input(type, data):
    return re.fullmatch(type, data)

# Get user preferences and request available flights from all airlines


def search_flights():
    print('Flight search')
    departure_airport = input('Departure airport: ')
    arrival_airport = input('Arrival airport: ')
    date_and_time = input('Preffered Date and Time: ')
    print('Summary of choices: ')
    print(f'Departure airport: {departure_airport}')
    print(f'Arrival airport: {arrival_airport}')
    print(f'Date and Time: {date_and_time}')
    confirm = input('Confirm? (y/n): ')
    if confirm == 'y':
        print('Booking flight...')
    else:
        print('Booking cancelled')

# Request user reference and last name to manage booking


def manage_booking():
    print('Manage booking')
# Proces payment


def process_payment():
    print("Processing payment...")

# Main method


def main():
    user_choice = ''
    while user_choice != '3':
        user_choice = input(
            'Hello! Please choose an option: \n1. Book flight\n2. Manage booking\n3. Quit\nYour choice:')
        if user_choice == '1':
            search_flights()
        elif user_choice == '2':
            manage_booking()
        elif user_choice == '3':
            print('Thank you for using our service!')
            break


main()
