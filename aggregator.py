import os
import sys
import requests
import re
import getpass

# Available airlines and payment providers
airline_apis = {'Emirates': 'https://sc20srn.pythonanywhere.com/emirates_api'}
search_endpoint = '/searchFlight'
payment_provider_apis = {}

# Sort by cheapest


def sort_by_cheapest(flights):
    return sorted(flights, key=lambda flight: flight['price'])

# Define regular expressions


email_regex = r'^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$'
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

# Validate input


def validate_input(type, data):
    return re.fullmatch(type, data)

# Format data


def format_date(date):
    day, month, year = re.split('/|-|\.', date)
    formatted_date = f'{year}-{month}-{day}'
    return formatted_date

# Get user preferences and request available flights from all airlines


def search_flights():
    print('Flight search')
    departure_airport = input('Departure airport: ')
    arrival_airport = input('Arrival airport: ')
    # Continuosly check for valid date
    while True:
        date = input('Preffered Date: ')
        if not validate_input(date_regex, date):
            print('Invalid date format.\nPlease supply date in one of the following formats:\ndd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy')
        else:
            print('\nSummary of choices: ')
            print('-------------------')
            print(f'Departure airport: {departure_airport}')
            print(f'Arrival airport: {arrival_airport}')
            print(f'Date: {date}')
            print('-------------------')
            confirm = input('Confirm? (y/n): \n')
            if confirm == 'y':
                # Send a request to airlines and list available flights
                params = {'departure_location': departure_airport,
                          'arrival_location': arrival_airport, 'departure_date': format_date(date)}
                for airline, url in airline_apis.items():
                    search_url = url + search_endpoint
                    response = requests.get(search_url, params=params)
                    if response.status_code == 200:
                        print(f'Available flights from {airline}:')
                        flights = response.json()
                        for flight in flights:
                            print(flight)
                        print('\n')
                    else:
                        print(f'Error: {response.status_code}')
                print('Available flights:\n')
                book_flight()
                break
            else:
                print('Booking cancelled\n')
                break


def book_flight():
    print('Booking flight...')
    first_name = input('First name: ')
    last_name = input('Last name: ')
    while True:
        email = input('Email: ')
        if not validate_input(email_regex, email):
            print('Invalid email format. Please try again.')
        else:
            phone_num = input('Phone number: ')
            if not validate_input(phone_num_regex, phone_num):
                print('Invalid phone number format. Please try again.')
            else:
                print('Booking details summary:')
                print('------------------------')
                print(f'First name: {first_name}')
                print(f'Last name: {last_name}')
                print(f'Email: {email}')
                print(f'Phone number: {phone_num}')
                print('------------------------')
                confirm = input('Confirm? (y/n): \n')
                if confirm == 'y':
                    # TODO send booking details to airline api
                    print('Booking successful!\n')
                    break
                else:
                    print('Booking cancelled\n')
                    break

# Manage booking and helper methods


def change_name():
    new_name = input('Enter new name: ')
    # TODO send new name to airline api
    print(f'Name successfully changed to {new_name}!')


def cancel_flight():
    print('Cancelling flight...')

# pay_by_card(amount)


def pay_by_card():
    print('Card payment\n')
    while True:
        card_num = input('Card number: ')
        if not validate_input(card_regex, card_num):
            print('Invalid card number format. Please try again.')
        else:
            cvv = input('CVV: ')
            if not validate_input(cvv_regex, cvv):
                print('Invalid CVV format. Please try again.')
            else:
                expiry_date = input('Expiry date: ')
                if not validate_input(date_regex, expiry_date):
                    print('Invalid date format. Please try again.')
                else:
                    # TODO send a request to payment provider api
                    print('Payment successful!\n')
                    break


def pay_with_klarna():
    print('Klarna payment\n')
    while True:
        email = input('Email: ')
        if not validate_input(email_regex, email):
            print('Invalid email format. Please try again.')
        else:
            password = getpass.getpass('Password: ')
            # TODO send a request to payment provider api
            print('Payment successful!\n')
            break


def process_payment():
    print('Please pick a payment method:\n')
    payment_method = input(
        '1. Card\n2. Klarna\n3. Go back\n4. Exit\nYour choice: ')
    if payment_method == '1':
        pay_by_card()
    elif payment_method == '2':
        pay_with_klarna()
    elif payment_method == '3':
        print('\nReturning to manage booking...\n')
        manage_booking()
    elif payment_method == '4':
        exit()
    else:
        print('\nInvalid choice. Returning to manage booking...\n')
        manage_booking()


def view_booking():
    print('Requesting booking details from airline...')


def manage_booking():
    print('Manage booking\n')
    while True:
        booking_ref = input('\nEnter your booking reference: ')
        if not validate_input(booking_ref_regex, booking_ref):
            print('\nInvalid booking reference.Please check your details and try again.')
        else:
            last_name = input('\nEnter your last name: ')
            # TODO check if booking exists and proceed to manage booking
            user_choice = ''
            while user_choice != '5':
                user_choice = input(
                    'Please choose an option:\n\n1. Change name\n2. Cancel flight\n3. Pay\n4. View Booking\n5. Back\n\nYour choice: ')
                if user_choice == '1':
                    change_name()
                elif user_choice == '2':
                    cancel_flight()
                elif user_choice == '3':
                    process_payment()
                elif user_choice == '4':
                    view_booking()
                elif user_choice == '5':
                    print('\nReturning to main menu...\n')
                    break
            break

# Exit function


def exit():
    print("Exiting...")
    sys.exit(0)

# Main method


def main():
    user_choice = ''
    while user_choice != '3':
        user_choice = input(
            'Hello! Please choose an option:\n\n1. Book flight\n2. Manage booking\n3. Quit\n\nYour choice: ')
        if user_choice == '1':
            search_flights()
        elif user_choice == '2':
            manage_booking()
        elif user_choice == '3':
            print('\nThank you for using our service!')
            exit()


main()
