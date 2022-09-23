
# input data: 
# student: id, name, gender, isSecondYear, nationality, main language, sleep_score, temp_score, study_score
# available rooms: no of 4rooms, no of 2rooms
# two categories of allocation rules: required and preferences

# students would be added automatically/through excel
DEBUG_STUDENTS = [[0, "Yannick", "m", True, "de", "german", 4, 1, 5]]


import pycountry

class Student():
    def __init__(self, id, name, gender, isSecondYear, nationality, main_language, sleep_score, temp_score, study_score):
        self.id = id
        self.name = name
        self.gender = gender
        self.isSecondYear = isSecondYear
        self.nationality = pycountry.countries.get(alpha_2 = nationality)
        self.main_language = pycountry.languages.get(alpha_2=main_language)
        self.sleep_score = sleep_score
        self.temp_score = temp_score
        self.study_score = study_score

    def __str__(self):
        print("This is {1} with\n\tID {0}\n\tgender {2}\n\t isSecondYear {3}\n\tnationality {4} \n\tmain language {5}\n\tscores: {6}, {7} {8}\n".format(self.id,self.name,self.gender,self.isSecondYear,self.nationality,self.main_language,self.sleep_score,self.temp_score,self.study_score))

    def isGerman(self):
        return self.nationality == pycountry.countries.get("de")
            

class Room_Allocator():

    def __init__(self):
        self.double_rooms = 8
        self.first_floor_rooms = 24
        self.second_floor_rooms = 24

        self.all_students = []
        self.add_students()

        print(self.all_students[0])



    def add_students(self):

        for i in range(len(DEBUG_STUDENTS)):
            self.all_students.append(Student( DEBUG_STUDENTS[i][0], 
                                                DEBUG_STUDENTS[i][1], 
                                                DEBUG_STUDENTS[i][2], 
                                                DEBUG_STUDENTS[i][3], 
                                                DEBUG_STUDENTS[i][4], 
                                                DEBUG_STUDENTS[i][5], 
                                                DEBUG_STUDENTS[i][6], 
                                                DEBUG_STUDENTS[i][7], 
                                                DEBUG_STUDENTS[i][8] ))
        


    def required_rules(self):
        pass
    

Room_Allocator()
