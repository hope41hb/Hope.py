class GradeManager:
    def __init__(self):
        self.data = {}

    def add_student(self, name, math, cs, physics):
        self.data[name] = {
            "Math": math,
            "CS": cs,
            "Physics": physics
        }
    #Delete student; return False if the student does not exist
    def delete_student(self, name):
        if name not in self.data:
            return False
        else:
            del self.data[name]
            return True

    def get_average_and_level(self, name):
        #If the student's name is not in the data dictionary, return None.
        if name not in self.data:
            return None, None

        #Retrieve the student's grade dictionary
        scores = self.data[name]
        #Retrieve the student's grade from dictionary value
        avg = sum(scores.values()) / len(scores)

        if avg >= 80:
            level = "A"
        elif 80 > avg >= 70:
            level = "B"
        else:
            level = "C"

        return avg, level
