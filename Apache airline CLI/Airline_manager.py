from Airline_task import airline_task
import json

#Manages all airline seat operations
class AirlineManager:
    # Initialize the AirlineManager
    def __init__(self, file_name="airline.json"):
        self.seat = None
        self.file_name = file_name
        self.airline_tasks = []
        self.load()

        #If no data exists, create initial seat layout
        if not self.airline_tasks:
            self.initialize()
            self.save()

    #Create 480 seats (6 rows × 80 seats)
    def initialize(self):
        self.airline_tasks = []
        # Seats 77 and 78 in rows D, E, F are marked as storage ("S"), All other seats are free ("F")
        for row in ["A","B","C","D","E","F"]:
            for num in range(1,81):
                seat_number = f"{num}{row}"
                if row in ["D","E","F"] and num in[77,78]:
                    seat_status = "S"
                else:
                    seat_status = "F"

                self.airline_tasks.append(airline_task(seat_number, seat_status))


    def find_seat(self, seat_number):
        #Search and return the seat object by seat number
        for seat in self.airline_tasks:
            if seat.seat_number == seat_number:
                return seat
        #Returns None if seat does not exist
        return None

    #Check the current status of a seat
    def check_availability(self, seat_number):
        seat = self.find_seat(seat_number)
        if seat.seat_status == "F":
           return f"{seat_number} is free"
        elif seat.seat_status == "R":
           return f"{seat_number} is booked"
        elif seat.seat_status == "S":
           return f"{seat_number} is a storage area"
        return None

    #Book a seat if it is free, changes seat status from "F" to "R"
    def book_a_seat(self, seat_number):
        seat = self.find_seat(seat_number)
        if seat is None:
            return f"seat {seat_number} not exist"
        elif seat.seat_status == "F":
           seat.seat_status = "R"
           self.save()
           return f"Booking successfully"
        elif seat.seat_status == "R":
           return f"Seat currently booked"
        elif seat.seat_status == "S":
           return f"This seat is a storage area"
        return None

    #Release a booked seat, changes seat status from "R" to "F"
    def free_a_seat(self, seat_number):
        seat = self.find_seat(seat_number)
        if seat is None:
            return f"seat {seat_number} not exist"
        elif seat.seat_status == "R":
           seat.seat_status = "F"
           self.save()
           return f"Release successfully"
        elif seat.seat_status == "F":
           return f"Seat is not currently booked"
        elif seat.seat_status == "S":
           return f"This seat is a storage area"
        return None

    #Display all currently booked seats
    def show_booking (self):
        booked = []
        for seat in self.airline_tasks:
            if seat.seat_status == "R":
               booked.append(seat.seat_number)
        if not booked:
            return "No seats are currently booked."

        return "Booked seats:" + "\n".join(booked)

    #Save all seat data to JSON file
    def save(self):
        with open(self.file_name, "w") as f:
            json.dump([t.to_dict_airline() for t in self.airline_tasks], f, indent=4)

    #Load seat data from JSON file, if file does not exist, create empty list
    def load(self):
        try:
            with open(self.file_name, "r") as f:
                data = json.load(f)
                self.airline_tasks = [airline_task(**d) for d in data]
        except Exception as e:
            print("Load error:", e)
            self.airline_tasks = []


