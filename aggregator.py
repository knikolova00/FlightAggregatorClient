import os


def book_flight():
    print('Book flight')


def manage_booking():
    print('Manage booking')


user_choice = ''
while user_choice != '3':
    user_choice = input(
        'Hello! Please choose an option: \n1. Book flight\n2. Manage booking\n3. Quit\nYour choice:')
    if user_choice == '1':
        book_flight()
    elif user_choice == '2':
        manage_booking()
    elif user_choice == '3':
        print('Thank you for using our service!')
        break
