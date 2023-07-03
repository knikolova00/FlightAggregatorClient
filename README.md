# Flight aggregator client
## Kalina Nikolova, 2023
**Developed as part of the Web Services and Web Data COMP module at the University of Leeds, taught by Dr Mohammad Ammar Alsalka.**


This file contains instructions for using aggregator.py created by Kalina Nikolova
for COMP3011 Web Services and Web Data, Coursework 2, 2023.

The application has been designed to allow communication between web services providing
flight booking and payment capabilities.

## Pre-requisites:
- There is a ```requirements.txt``` file which contains all external libraries which are used by the client.
They all need to be installed before running the application. Please note that the solution has been testes on the
school machines which run a python version <3.7. If testing on these, please install ```requirements_lab_machines.txt``` instead.
- Run ```pip install -r requirement.txt``` to install the required packages.
- If you prefer to install these in a virtual environment, firstly run ```python3 -m venv <name_of_venv>```.
This creates a new virtual environment which can be activated with ```.\venv\Scripts\activate``` on Windows
and ```source <venv_directory>/bin/activate``` on Unix based operating systems.

## Other notes:
- There is an example transcript of the application's usage in the file ```example_transcript.txt```.

## Usage:
1. The application is started by running ```python aggregator.py``` in a terminal window.
2. This should display a menu with three options - 1.Book a flight, 2. Manage Booking and 3.Quit.
3. Supplying a number '1', '2' or '3' and pressing 'Enter' results in the invocation of the service
associated with that number.

### Book a flight:

#### Flight searching parameters: 

Example 1
Departure Airport: Dubai
Arrival Airport: Manchester
Preferred Date: 15/05/2023

Example 2 (generates flights from 3 airlines)
Departure Airport: London
Arrival Airport: Singapore
Preferred Date: 01/06/2023

After entering these, you will be asked to confirm your choice. Please choose 'y' and press enter to continue.
You will get a list of flights and a number associated with those. Please choose a number and press enter.

#### User data parameters:
First Name: Your first name
Last Name: Your last name
Email: follow the pattern 'ex@mail.com'
Phone number: 11 digits, 07896781231

You will be asked to confirm once more. On confirmation, a booking summary is displayed in the terminal and also saved as a pdf. 
The pdf is saved in the same directory as the application. After that, you will be asked if you want to pay for the booking. You can
choose 'y' or 'n'. If you choose 'y', you will be asked to choose a payment provider. Please enter a number and press enter. Then, you will be
prompted to choose a payment method. If you choose '1', you will be asked to enter your card details. If you choose '2', you will be asked to enter
an email and a password. Once the details have been entered, you will either get a confirmation message or an error message.

#### Payment parameters:

For PaymentOne 

Card Payment:

EasyPay:
Card Number: 5105105105105100
CVV: 789
Expiry Date: 1030

SwiftPay:
Card Number: 2323232323232323
CVV: 123
Expiry Date: 0529

Payment by email and password:

PaymentOne:
Email:test@test.com
password: test (Note that the password is hidden when you type it in the terminal)

SwiftPay:
Email: shaji.febin@yahoo.com
password: Febin123


### Manage Booking:

#### Required parameters:
1. Booking reference: 3 letters and 4 digits, e.g. ABC1234 (Take a note when making a booking in order to use it here)
2. Last Name: The name you used to make a booking
3. Airline: The airline you booked with
(All of these are also saved to the pdf document when you make a booking)

#### Available features: 
1. Change Name:
New First Name: Pick a new first name
New Last Name: Pick a new last name
You will get a confirmation once complete.
2. Cancel Booking:
You are asked to confirm and then you get a confirmation message.
3. Pay:
Check Book a flight from above for payment parameters.
4. View Booking:
Displays summary similar to when completing a booking via the Book flight option.

