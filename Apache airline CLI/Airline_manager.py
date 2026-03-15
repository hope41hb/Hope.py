from Airline_task import airline_task
import sqlite3
import random
import string

# Manages all airline seat operations
# such as booking seats, checking availability, adding drinks, etc.
class AirlineManager2:
    # Initialize the AirlineManager
    # Constructor: runs automatically when the class is created
    # It prepares the database and initializes all seats
    def __init__(self):
        self.seat = None
        # List that stores all seat objects (480 seats)
        self.airline_tasks = []
        # Connect to SQLite database file
        # If the file does not exist, SQLite will automatically create it
        self.conn = sqlite3.connect("airline.db")
        # Create a "database manipulation tool"
        # Cursor object allows to execute SQL commands
        self.cursor = self.conn.cursor()
        # Create the booking table if it does not already exist
        self.create_table()

        # If no data exists, create initial seat layout
        if not self.airline_tasks:
            self.initialize()

    # To execute an SQL command in the database.
    # This table stores passenger booking information
    def create_table(self):
        self.cursor.execute("""
         CREATE TABLE IF NOT EXISTS booking (
                booking_reference TEXT PRIMARY KEY,
                passport_number TEXT,
                first_name TEXT,
                last_name TEXT,
                seat_number TEXT,
                seat_status TEXT,
                drink TEXT
                )
         """)
        #Actually written to the database file
        self.conn.commit()


    #Create 480 seats (6 rows × 80 seats)
    def initialize(self):
        self.airline_tasks = []
        # Seats 77 and 78 in rows D, E, F are marked as storage ("S"), All other seats are free ("F")
        for row in ["A","B","C","D","E","F"]:
            for num in range(1,81):
                seat_number = f"{num}{row}"
                drink = None
                if row in ["D","E","F"] and num in[77,78]:
                    seat_status = "S"
                else:
                    seat_status = "F"

                # Create seat object and store in list
                self.airline_tasks.append(airline_task(seat_number, seat_status, drink))


    def find_seat(self, seat_number):
        #Search and return the seat object by seat number
        for seat in self.airline_tasks:
            if seat.seat_number == seat_number:
                return seat
        # Returns None if seat does not exist
        return None

    # Check the current status of a seat
    def check_availability(self, seat_number):

        seat = self.find_seat(seat_number)

        # Seat does not exist
        if seat is None:
            return f"seat {seat_number} not exist"

        # Storage seats cannot be booked
        if seat.seat_status == "S":
            return f"{seat_number} is a storage area"

        # Query database to check if seat is booked
        self.cursor.execute(
            "SELECT seat_number FROM booking WHERE seat_number = ?",
            (seat_number,)
        )

        result = self.cursor.fetchone()

        # If database contains this seat
        if result:
            return f"{seat_number} is booked"
        # Otherwise seat is available
        else:
            return f"{seat_number} is free"

    # Generate a random booking reference
    # Format: 8 characters (A-Z + 0-9)
    def generate_booking_reference(self):
        #Use uppercase letters + numbers
        character = string.ascii_uppercase + string.digits

        # Randomly choose 8 times
        while True:
            reference = ''.join(random.choice(character) for _ in range(8))
            # Check if the data already exists
            self.cursor.execute(
                "SELECT booking_reference FROM booking WHERE booking_reference = ?",
                (reference,)
            )
            # If reference does not exist in database
            if not self.cursor.fetchone():
                return reference

    # Book a seat for a passenger
    def book_a_seat(self, seat_number, passport, first_name, last_name):

        seat = self.find_seat(seat_number)

        if seat is None:
            return f"seat {seat_number} not exist"

        if seat.seat_status == "S":
            return "This seat is storage"

        # Check if the database has been subscribed
        self.cursor.execute(
            "SELECT seat_number FROM booking WHERE seat_number = ?",
            (seat_number,)
        )

        if self.cursor.fetchone():
            return "seat already booked"

        # Generate booking reference
        booking_reference = self.generate_booking_reference()

        # Insert booking information into database
        self.cursor.execute("""
            INSERT INTO booking
            (booking_reference, passport_number, first_name, last_name, seat_number, seat_status, drink)
            VALUES (?,?,?,?,?,?,?)
        """, (booking_reference, passport, first_name, last_name, seat_number, "R", None))

        # Save database changes
        self.conn.commit()

        # Update seat status in memory
        seat.seat_status = "R"

        return f"Booking successfully. Reference {booking_reference}"

    # Add a drink selection to a booked seat
    def drink(self, seat_number, drink):

        seat = self.find_seat(seat_number)

        # Seat does not exist
        # if seat is None:
        #     return "seat not exist"

        # Check if seat is booked
        self.cursor.execute(
            "SELECT seat_number FROM booking WHERE seat_number = ?",
            (seat_number,)
        )

        result = self.cursor.fetchone()#find data

        if not result:
            return "There is no passenger in this seat"

        if drink in ["coke","apple juice","orange juice","sparkling water"]:
            # Update memory data
            # Update drink choice in database
            self.cursor.execute("""
                            UPDATE booking
                            SET drink = ?
                            WHERE seat_number = ?
                        """, (drink, seat_number))

            self.conn.commit()
            seat.drink = drink
            return "Drink added successfully"
        else:
            return "We don't have this drink"


    #Release a booked seat, changes seat status from "R" to "F"
    def free_a_seat(self, seat_number, reference):

        seat = self.find_seat(seat_number)

        if seat is None:
            return f"seat {seat_number} not exist"

        # Check booking reference from database
        self.cursor.execute(
            "SELECT booking_reference FROM booking WHERE seat_number = ?",
            (seat_number,)
        )

        row = self.cursor.fetchone()

        if not row:
            return "Seat is not booked"

        # If reference does not match
        if row[0] != reference:
            return "Reference incorrect"

        # Delete booking record
        self.cursor.execute(
            "DELETE FROM booking WHERE seat_number = ?",
            (seat_number,)
        )

        self.conn.commit()

        # Update seat status in memory
        seat.seat_status = "F"

        return "Seat freed successfully"

    #Display all currently booked seats
    def show_booking(self):

        # Query database for all bookings
        self.cursor.execute(
            "SELECT seat_number, drink FROM booking"
        )

        rows = self.cursor.fetchall()

        if not rows:
            return "No seats are currently booked."

        result = []

        # Format booking output
        for seat_number, drink in rows:
            result.append(f"{seat_number} drink:{drink}")

        return "Booked seats:\n" + "\n".join(result)









