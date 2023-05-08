This file contains instructions for using aggregator.py created by Kalina Nikolova
for COMP3011 Web Services and Web Data, Coursework 2, 2023.

The application has been designed to allow communication between web services providing
flight booking and payment capabilities.

Pre-requisites:
- There is a 'requirements.txt' file which contains all external libraries which are used by the client.
They all need to be installed before running the application. 
- Run ```pip install requirement.txt``` to install the required packages.
- If you prefer to install these in a virtual environment, firstly run ```python3 -m venv <name_of_venv>```.
This creates a new virtual environment which can be activated with ```.\venv\Scripts\activate``` on Windows
and ```source <venv_directory>/bin/activate``` on Unix based operating systems.

Usage:
1. The application is started by running ```python aggregator.py``` in a terminal window.
2. This should display a menu with three options - 1.Book a flight, 2. Manage Booking and 3.Quit.
3. Supplying a number '1', '2' or '3' and pressing 'Enter' results in the invocation of the service
associated with that number.

Book a flight:

1. Flight searching parameters: 
Departure Airport: Dubai
Arrival Airport: Manchester
Preferred Date: 15/05/2023

After entering these, you will be asked to confirm your choice. Please choose 'y' and press enter to continue.
You will get a list of flights and a number associated with those. Please choose a number and press enter.

2. User data parameters:
First Name: Your first name
Last Name: Your last name
Email: follow the pattern 'ex@mail.com'
Phone number: 11 digits, 07896781231

You will be asked to confirm once more. On confirmation, a booking summary is displayed in the terminal and also saved as a pdf.


