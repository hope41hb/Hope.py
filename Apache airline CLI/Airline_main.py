from Airline_manager2 import AirlineManager2

todo = AirlineManager2()
#Main user interface for the Airline Booking System，CLI
class main:
    #Create an instance of AirlineManager


    #Main menu loop
    #The program runs continuously until the user chooses to exit.
    while True:
          #Display menu options
          print("\n====== Apache airlines ======")
          print("1. Availability of seat")
          print("2. Book a seat")
          print("3. Free a seat")
          print("4. Booking status")
          print("5. Choosing drink")
          print("6. Exit")

          #Get user input and remove extra spaces
          choice = input("Enter your choice:").strip()

          #Option 1: Check seat availability
          if choice == "1":
             num = input("Please enter your seat's number(e.g. 1A, 1B....) :").strip().upper()
             print(todo.check_availability(num))

          #Option 2: Book a seat
          elif choice == "2":
             num = input("Please enter your seat's number:").strip().upper()
             passport = input("Passport number: ")
             first = input("First name: ")
             last = input("Last name: ")
             print(todo.book_a_seat(num, passport, first, last))

          #Option 3: Free a seat
          elif choice == "3":
              booking_reference = input("Please enter your seat's booking reference:").strip()
              num = input("Please enter the seat number to free: ").strip().upper()
              print(todo.free_a_seat(num, booking_reference))

          #Option 4: Show all booked seats
          elif choice == "4":
              print(todo.show_booking())

          #Option 5: Choosing drink
          elif choice == "5":
              num = input("Which seat are you in?:").strip().upper()
              drink = input("What drinks do you want? Coke/ Apple juice/ Orange juice/ sparkling water").strip().lower()
              print(todo.drink(num,drink))

          #Option 6: Exit program
          elif choice == "6":
              print("Goodbye.")
              break


