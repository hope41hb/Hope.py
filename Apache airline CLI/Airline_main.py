from Airline_manager import AirlineManager

#Main user interface for the Airline Booking System，CLI
class main:
    #Create an instance of AirlineManager
    todo = AirlineManager()

    #Main menu loop
    #The program runs continuously until the user chooses to exit.
    while True:
          #Display menu options
          print("\n====== Apache airlines ======")
          print("1. Availability of seat")
          print("2. Book a seat")
          print("3. Free a seat")
          print("4. Booking status")
          print("5. Exit")

          #Get user input and remove extra spaces
          choice = input("Enter your choice:").strip()

          #Option 1: Check seat availability
          if choice == "1":
             num = input("Please enter your seat's number:").strip().upper()
             print(todo.check_availability(num))

          #Option 2: Book a seat
          elif choice == "2":
             num = input("Please enter your seat's number:").strip().upper()
             print(todo.book_a_seat(num))

          #Option 3: Free a seat
          elif choice == "3":
              num = input("Please enter the seat number to free: ").strip().upper()
              print(todo.free_a_seat(num))

          #Option 4: Show all booked seats
          elif choice == "4":
              print(todo.show_booking())

          #Option 5: Exit program
          elif choice == "5":
              print("Goodbye.")
              break


