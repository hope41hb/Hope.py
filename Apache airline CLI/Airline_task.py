# Stores seat number and current seat status
class airline_task():

      #Initialize a seat with its number and status
      def __init__(self, seat_number, seat_status):
          self.seat_number = seat_number
          self.seat_status = seat_status

      # Convert the seat object to a dictionary
      def to_dict_airline(self):
          return {
              "seat_number": self.seat_number,
              "seat_status": self.seat_status
          }