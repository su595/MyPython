from random import randint
import xlrd
from datetime import datetime
import matplotlib.pyplot as plt

# this should be done with a database, so I should not put too much effort into making this program easy to use

PATH = "/home/yannick/git-repos/MyPython/math programs/investi.xls" # .xls only
DATA_RANGE = (15, 559) # tuple of (start_num, end_num) !starting from 0, subtract 1 from line number
COLUMNS = {"year": "B", "id": "C", "A_or_R": "E", "m_score": "F", "e_score": "G"} # dict with "data name": "column charachter (A-ZZ)"
MODULO_NUMBER = 10
# For blank values, I just set a score of 0

def make_data_list(sheet, data_range, columns):
    
    data_list = []

    for i_line in range(data_range[0], data_range[1]):
        line = []
        for key in columns.keys():
            line.append(sheet.cell_value(rowx=i_line, colx=columns[key]))
        
        data_list.append(line)
    
    return data_list

def column_to_number(col): # char of colum name, only defined from A to ZZ
    col = col.upper() # make all chars uppercase
    
    if len(col) == 1:
        return ord(col) - 65 # ord returns the ascii value which has an offset of 65

    elif len(col) == 2:
        value = (26 * (ord(col[0])-64)) + (ord(col[1])-65) # first char is like offset of 26 columns
        # A means zero as the second char, but as the first char it stands for + 1*26, so we need to subtract only 64
        return value
    
    return -1 # if column name is too long, return -1

def convert_columns(columns):
    # convert column letters to numbers
    for key in columns.keys():
        columns[key] = column_to_number(columns[key])

    return columns

def replace_something(list, replace, replaceWith): # two dimensional list, returns modified list number of items replaced
    counter = 0
    to_be_replaced = []

    for i1 in range(len(list)):
        for i2 in range(len(list[i1])):
            if list[i1][i2] is replace:              
                to_be_replaced.append([i1, i2])
                counter += 1
    
    for bad in to_be_replaced:
        list[bad[0]][bad[1]] = replaceWith
    
    return list

def make_columns_for_list(columns):
    i = 0
    list_columns = {}
    for key in columns.keys():
        list_columns[key] = i
        i += 1
    
    return list_columns

def get_average_scores(list, english): # returns a tuple of (A scores, R scores)
    sum_of_english_A = 0
    num_of_english_A = 0
    sum_of_english_R = 0
    num_of_english_R = 0

    if english:
        key = "e_score"
    else:
        key = "m_score"

    for student in list:
        
        if student[columns_for_list["A_or_R"]] == "A":
            sum_of_english_A += student[columns_for_list[key]]
            num_of_english_A += 1
        elif student[columns_for_list["A_or_R"]] == "R":
            sum_of_english_R += student[columns_for_list[key]] # english is the 5th column as defined above
            num_of_english_R += 1
        else:
            print("wrong a or r")

    if num_of_english_R == 0 or num_of_english_A == 0:
        return None

    return (sum_of_english_A/num_of_english_A, sum_of_english_R/num_of_english_R)

def get_error(real_value, value):
    return ((value-real_value)/real_value)*100


print(randint(0,6))
start_time = datetime.now()

book = xlrd.open_workbook(PATH)
sh = book.sheet_by_index(0)

columns = convert_columns(COLUMNS)
columns_for_list = make_columns_for_list(columns)
list_of_students = make_data_list(sh, DATA_RANGE, columns)
list_of_students = replace_something(list_of_students, '_', 0) # what should a bad entry be replaced with?? or just discard the entire data point?

new_list = []

for i in range(len(list_of_students)):
    if i % MODULO_NUMBER == 0:
        new_list.append(list_of_students[i])


    average_real_scores = get_average_scores(list_of_students, True)
    average_sample_scores = get_average_scores(new_list, True)



        

print("This took a time of {} ".format(datetime.now()-start_time))


print(len(list_of_students))
print(len(new_list))

average_sample_scores = get_average_scores(new_list, True)
average_sample_scores_M = get_average_scores(new_list, False)
average_real_scores = get_average_scores(list_of_students, True)
error_A = get_error(average_real_scores[0], average_sample_scores[0])
error_R = get_error(average_real_scores[1], average_sample_scores[1])
print("The average sample English scores are {:.4} for A-students and {:.4} for R-students".format(average_sample_scores[0], average_sample_scores[1]))
print("The average sample Math scores are {:.4} for A-students and {:.4} for R-students".format(average_sample_scores_M[0], average_sample_scores_M[1]))
print("The sampled and real value differ by {:.2} percent for A-students and {:.2} percent for R-students".format(error_A, error_R))



 



