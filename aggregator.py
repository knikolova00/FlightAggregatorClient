# Built in modules
import os
import sys
import getpass
# Require installation - please check 'requirements.txt'
import requests
import re
from reportlab.pdfgen import canvas

# Available airlines and payment providers
airline_apis = {'Emirates': 'https://sc20srn.pythonanywhere.com/emirates_api'}
search_endpoint = '/searchFlight'
book_endpoint = '/bookFlight/'
view_endpoint = '/getBooking/'
edit_endpoint = '/editBooking/'
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

# Format date


def format_date(date):
    day, month, year = re.split('/|-|\.', date)
    formatted_date = f'{year}-{month}-{day}'
    return formatted_date

# Format Flight response


def format_flights(response):
    for flight in response.json():
        print(f"Flight {flight['id']}: {flight['airline']} - Departing from {flight['departure_airport']} on {flight['date']} at {flight['departure_time']}. Arriving at {flight['arrival_airport']} at {flight['arrival_time']}. Duration: {flight['duration']} hours. Price: £{flight['price']}")

# Format booking info and save to PDF


def format_booking(booking):
    print(f"Booking reference: {booking['reference_id']}")
    print(f"Flight: {booking['flight_id']}")
    print(f"Date: {booking['date']}")
    print(f"First name: {booking['first_name']}")
    print(f"Last name: {booking['last_name']}")
    print(f"Phone number: {booking['phone_no']}")
    print(f"Email: {booking['email']}")
    print(f"Price: {booking['price']}")
    print(f"Payment confirmed: {booking['confirmed']}")

    # Create a new PDF file
    file_name = f"{booking['last_name']}_{booking['reference_id']}.pdf"
    pdf_file = canvas.Canvas(file_name)

    # Set the font size and style
    pdf_file.setFont('Helvetica', 12)

    # Write the booking information to the PDF
    pdf_file.drawString(
        100, 750, f"Booking reference: {booking['reference_id']}")
    pdf_file.drawString(100, 700, f"Flight: {booking['flight_id']}")
    pdf_file.drawString(100, 650, f"Date: {booking['date']}")
    pdf_file.drawString(100, 600, f"First name: {booking['first_name']}")
    pdf_file.drawString(100, 550, f"Last name: {booking['last_name']}")
    pdf_file.drawString(100, 500, f"Phone number: {booking['phone_no']}")
    pdf_file.drawString(100, 450, f"Email: {booking['email']}")
    pdf_file.drawString(100, 400, f"Price: {booking['price']}")
    pdf_file.drawString(100, 350, f"Payment confirmed: {booking['confirmed']}")

    # Save and close the PDF file
    pdf_file.save()
    print('-------------------\n')
    print(f'Booking confirmation saved to {file_name}')
    print('\n')


# Get user preferences and request available flights from all airlines


def search_flights():
    print('Flight search')
    departure_airport = input('Departure airport: ')
    arrival_airport = input('Arrival airport: ')
    # Continuosly check for valid date
    while True:
        date = input('Prefered Date: ')
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
                        print('Available flights:\n')
                        format_flights(response)
                        print('\n')
                    else:
                        print(f'Error: {response.status_code}')
                flight_id = input('Enter flight id to book: ')
                for flight in response.json():
                    if flight['id'] == int(flight_id):
                        print(
                            f"You have selected flight {flight_id} departing on {flight['date']}.\n")
                        book_flight(
                            flight['id'], flight['date'], flight['airline'])
                        break
                break
            else:
                print('Booking cancelled\n')
                break


def book_flight(flight_id, date, airline):

    # Get the airline api url
    book_url = airline_apis[airline] + book_endpoint
    print(book_url)

    print('Booking flight...')
    first_name = input('First name: ')
    last_name = input('Last name: ')
    while True:
        phone_num = input('Phone number: ')
        if not validate_input(phone_num_regex, phone_num):
            print('Invalid phone number format. Please try again.')
        else:
            email = input('Email: ')
            if not validate_input(email_regex, email):
                print('Invalid email format. Please try again.')
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
                    params = {'flight_id': flight_id, 'date': date, 'first_name': first_name,
                              'last_name': last_name, 'phone_no': phone_num, 'email': email}
                    headers = {'Content-Type': 'application/json'}
                    response = requests.post(
                        book_url, params=params, headers=headers)
                    print('Request URL:', response.request.url)
                    print('Request method:', response.request.method)
                    print('Request headers:', response.request.headers)
                    print('Request body:', response.request.body)
                    if response.status_code == 200:
                        print('Booking successful!\n')
                        format_booking(response.json())
                        break
                    else:
                        print(f'Error: {response.status_code}-{response.text}')
                        exit()
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


def manage_booking():
    print('Manage booking\n')
    while True:
        booking_ref = input('\nEnter your booking reference: ')
        if not validate_input(booking_ref_regex, booking_ref):
            print('\nInvalid booking reference.Please check your details and try again.')
        else:
            last_name = input('\nEnter your last name: ')
            airline = input('\nEnter the airline you booked with: ')
            # Check if booking exists and proceed to manage booking
            params = {'reference_id': booking_ref, 'last_name': last_name}
            check_endpoint = airline_apis[airline] + view_endpoint
            response = requests.get(check_endpoint, params=params)
            if response.status_code == 200:
                user_choice = ''
                while user_choice != '5':
                    user_choice = input(
                        'Please choose an option:\n\n1. Change name\n2. Cancel flight\n3. Pay\n4. View Booking\n5. Back\n\nYour choice: ')
                    if user_choice == '1':
                        new_first_name = input('Enter new first name: ')
                        new_last_name = input('Enter new last name: ')
                        change_params = {'reference_id': booking_ref, 'last_name': last_name,
                                         'new_first_name': new_first_name, 'new_last_name': new_last_name}
                        change_endpoint = airline_apis[airline] + edit_endpoint
                        change_response = requests.put(
                            change_endpoint, params=change_params)
                        if change_response.status_code == 200:
                            print(
                                f'Name successfully changed to {new_first_name} {new_last_name}!')
                        else:
                            print(
                                f'Error: {change_response.status_code}-{change_response.text}')
                            exit()
                    elif user_choice == '2':
                        cancel_flight()
                    elif user_choice == '3':
                        process_payment()
                    elif user_choice == '4':
                        print('\nBooking details summary:')
                        print(
                            '------------------------')
                        format_booking(response.json())
                    elif user_choice == '5':
                        print('\nReturning to main menu...\n')
                        break
            else:
                print(
                    f'Error: {response.status_code}-{response.text}. Booking not found. Please try again.')
                manage_booking()
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
