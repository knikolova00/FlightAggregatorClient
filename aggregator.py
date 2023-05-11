# Built in modules
import os
import sys
import getpass
import json
# Require installation - please check 'requirements.txt'
import requests
import re
from reportlab.pdfgen import canvas

# Available airlines and payment providers
airline_apis = {'Emirates': 'https://sc20srn.pythonanywhere.com/emirates_api',
                'ryanAir': 'http://sc20sbz.pythonanywhere.com/api',
                'Aegean Airlines': 'http://sc19mkp.pythonanywhere.com/aegean',
                'Lufthansa': 'http://ed18r22c.pythonanywhere.com/lufthansa_api',
                }

#
payment_provider_apis = {
    'EasyPay': 'https://ed19ts3.pythonanywhere.com/pay/',
    'SwiftPay': 'http://ed192fs.pythonanywhere.com/pay/',
    'PayWithShan': 'https://ed19sehd.pythonanywhere.com/polls',
    'PayLink': 'https://sc20rmd.pythonanywhere.com/pay/'
}

# Define endpoints
search_endpoint = '/searchFlight/'
book_endpoint = '/bookFlight/'
view_endpoint = '/getBooking/'
edit_endpoint = '/editBooking/'
cancel_endpoint = '/cancelBooking/'
confirm_endpoint = '/confirmPayment/'

pay_by_email_endpoint = '/payEmail/'
pay_by_card_endpoint = '/payCard/'


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

# Sort by cheapest flight


def sort_by_cheapest(flights):
    return sorted(flights, key=lambda flight: float(flight['price']), reverse=False)

# Format Flight response


def format_flights(flights):
    try:
        sorted_flights = sort_by_cheapest(flights)
        for flight in sorted_flights:
            print(f"Flight {flight['id']}: {flight['airline']} - Departing from {flight['departure_airport']} on {flight['date']} at {flight['departure_time']}. Arriving at {flight['arrival_airport']} at {flight['arrival_time']}. Duration: {flight['duration']} hours. Price: £{flight['price']}")
            print('\n')
    except Exception as e:
        print('An error has occured.', e)
        exit()

# Format booking info and save to PDF


def format_booking(booking):
    print(f"Booking reference: {booking['reference_id']}")
    print(f"Flight: {booking['flight_id']}")
    print(f"Date: {booking['date']}")
    print(f"First name: {booking['first_name']}")
    print(f"Last name: {booking['last_name']}")
    print(f"Phone number: {booking['phone_no']}")
    print(f"Email: {booking['email']}")
    print(f"Price: £ {booking['price']}")

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
    try:
        departure_airport = input('Departure airport: ')
        arrival_airport = input('Arrival airport: ')
        # Continuosly check for valid date
        while True:
            date = input('Prefered Date(dd/mm/yyy, dd-mm-yyyy, dd.mm.yyyy): ')
            if not validate_input(date_regex, date):
                print(
                    'Invalid date format.\nPlease supply date in one of the following formats:\ndd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy')
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
                    print('Available flights:\n')
                    avail_flights = []
                    for airline, url in airline_apis.items():
                        search_url = url + search_endpoint
                        response = requests.get(search_url, params=params)
                        if response.status_code == 200:
                            flights = response.json()
                            for flight in flights:
                                avail_flights.append(flight)
                        else:
                            print(
                                f'Error: {response.status_code} - {response.text}')
                    if len(avail_flights) == 0:
                        print(
                            'No flights available! Please choose a different date.\n')
                        search_flights()
                    else:
                        format_flights(avail_flights)
                    flight_id = input('Enter flight id to book: ')
                    for flight in avail_flights:
                        if int(flight['id']) == int(flight_id):
                            print(
                                f"You have selected flight {flight_id} departing on {flight['date']}.\n")
                            book_flight(
                                flight['id'], flight['date'], flight['airline'], flight['price'])
                            break
                    break
                else:
                    print('Booking cancelled\n')
                    break
    except KeyboardInterrupt:
        print('\nExiting')

# Booking a flight


def book_flight(flight_id, date, airline, price):

    # Get the airline api url
    book_url = airline_apis[airline] + book_endpoint

    print('Booking flight...')
    try:
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
                        if response.status_code == 200 or response.status_code == 201:
                            print('Booking successful!\n')
                            format_booking(response.json())
                            payment = input("Continue to payment?(y/n): ")
                            if payment == 'y':
                                choose_payment_provider(
                                    airline, price, response.json()['reference_id'])
                            else:
                                print(
                                    'Payment cancelled. You can pay later via the Manage booking menu by supplying your booking reference and last name.\n')
                                exit()
                        else:
                            print(
                                f'Error: {response.status_code}-{response.text}')
                            exit()
                    else:
                        print('Booking cancelled\n')
                        break
    except KeyboardInterrupt:
        print('\nExiting')

# Manage booking and helper methods

# Card payment


def pay_by_card(payment_api, amount, airline, reference_id):
    try:
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
                    payment_link = payment_api + pay_by_card_endpoint
                    params = {'card_num': card_num, 'CVV': cvv, 'expiry_date': expiry_date,
                              'amount': amount}
                    response = requests.post(payment_link, json=params)
                    if response.status_code == 200 and response.json()['status'] == 200:
                        print(f'Payment of £{amount} successful!\n')
                        print(response.json())
                        confirmation_params = {'reference_id': reference_id, 'payment_id': response.json()[
                            'paymentId']}
                        confirmation_response = requests.post(
                            airline_apis[airline] + confirm_endpoint, params=confirmation_params)
                        if confirmation_response.status_code == 200:
                            print(f'Payment confirmed by {airline}!\n')
                            exit()
                        else:
                            print(
                                f'Error: {confirmation_response.status_code}-{confirmation_response.text}')
                            exit()
                    else:
                        print(
                            f'Error: {response.status_code}-{response.text}')
                        exit()
    except KeyboardInterrupt:
        print('\nExiting')


# Payment by email and password
def pay_by_email(payment_api, amount, airline, reference_id):
    try:
        print('Email and password payment\n')
        while True:
            email = input('Email: ')
            if not validate_input(email_regex, email):
                print('Invalid email format. Please try again.')
            else:
                password = getpass.getpass('Password: ')
                payment_link = payment_api + pay_by_email_endpoint
                params = {'email': email,
                          'password': password, 'amount': amount}
                response = requests.post(payment_link, json=params)
                if response.status_code == 200 and response.json()['status'] == 200:
                    print(f'Payment of £{amount} successful!\n')
                    print(response.json())
                    confirmation_params = {'reference_id': reference_id, 'payment_id': response.json()[
                        'paymentId']}
                    confirmation_response = requests.post(
                        airline_apis[airline] + confirm_endpoint, params=confirmation_params)
                    if confirmation_response.status_code == 200:
                        print(f'Payment confirmed by {airline}!\n')
                        exit()
                    else:
                        print(
                            f'Error: {confirmation_response.status_code}-{confirmation_response.text}')
                        exit()
                else:
                    print(f'Error: {response.status_code}-{response.text}')
                    exit()
    except KeyboardInterrupt:
        print('\nExiting')


# Choosing payment method
def process_payment(payment_api, price, airline, reference_id):
    try:
        print('Please pick a payment method:\n')
        payment_method = input(
            '1. Card\n2. Email and password payment\n3. Go back\n4. Exit\nYour choice: ')
        if payment_method == '1':
            pay_by_card(payment_api, price, airline, reference_id)
        elif payment_method == '2':
            pay_by_email(payment_api, price, airline, reference_id)
        elif payment_method == '3':
            print('\nReturning to manage booking...\n')
            manage_booking()
        elif payment_method == '4':
            exit()
        else:
            print('\nInvalid choice. Returning to manage booking...\n')
            manage_booking()
    except KeyboardInterrupt:
        print('\nExiting')

# Choosing payment provider


def choose_payment_provider(airline, price, reference_id):
    try:
        print('Please choose a payment provider:\n')
        payment_provider = input(
            '1.EasyPay\n2.SwiftPay\n3.PayWithShan\n4.PayLink\n5.Exit\nYour choice: ')
        if payment_provider == '1':
            payment_api = payment_provider_apis['EasyPay']
            process_payment(payment_api, price, airline, reference_id)
        elif payment_provider == '2':
            payment_api = payment_provider_apis['SwiftPay']
            process_payment(payment_api, price, airline, reference_id)
        elif payment_provider == '3':
            payment_api = payment_provider_apis['PayWithShan']
            process_payment(payment_api, price, airline, reference_id)
        elif payment_provider == '4':
            payment_api = payment_provider_apis['PayLink']
            process_payment(payment_api, price, airline, reference_id)
        else:
            exit()
    except KeyboardInterrupt:
        print('\nExiting')

# Manage booking functionality


def manage_booking():
    print('Manage booking\n')
    try:
        while True:
            booking_ref = input('\nEnter your booking reference: ')
            if not validate_input(booking_ref_regex, booking_ref):
                print(
                    '\nInvalid booking reference.Please check your details and try again.')
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
                            change_endpoint = airline_apis[airline] + \
                                edit_endpoint
                            change_response = requests.put(
                                change_endpoint, params=change_params)
                            if change_response.status_code == 200:
                                print(
                                    f'Name successfully changed to {new_first_name} {new_last_name}!')
                                break
                            else:
                                print(
                                    f'Error: {change_response.status_code}-{change_response.text}')
                                exit()
                        elif user_choice == '2':
                            confirm = input(
                                'Are you sure you want to cancel? (y/n): ')
                            if confirm == 'y':
                                cancel_flight_endpoint = airline_apis[airline] + \
                                    cancel_endpoint
                                cancel_params = {
                                    'reference_id': booking_ref, 'last_name': last_name}
                                cancel_response = requests.delete(
                                    cancel_flight_endpoint, params=cancel_params)
                                if cancel_response.status_code == 200:
                                    print('Flight successfully cancelled!')
                                    break
                                else:
                                    print(
                                        f'Error: {cancel_response.status_code}-{cancel_response.text}')
                                    exit()
                            else:
                                break
                        elif user_choice == '3':
                            choose_payment_provider(
                                airline, response.json()['price'], response.json()['reference_id'])
                        elif user_choice == '4':
                            print('\nBooking details summary:')
                            print(
                                '------------------------')
                            format_booking(response.json())
                            break
                        elif user_choice == '5':
                            print('\nReturning to main menu...\n')
                            break
                else:
                    print(
                        f'Error: {response.status_code}-{response.text}. Booking not found. Please try again.')
                    manage_booking()
                break
    except KeyboardInterrupt:
        print('\nExiting')

# Exit function


def exit():
    print("Exiting...")
    sys.exit(0)

# Main method


def main():
    print('Welcome to SkySavers!\n')
    user_choice = ''
    try:
        while user_choice != '3':
            user_choice = input(
                'Please choose an option:\n\n1. Book flight\n2. Manage booking\n3. Quit\n\nYour choice: ')
            if user_choice == '1':
                search_flights()
            elif user_choice == '2':
                manage_booking()
            elif user_choice == '3':
                print('\nThank you for using our service!')
                exit()
    except KeyboardInterrupt:
        print('\nExiting')


if __name__ == '__main__':
    main()
