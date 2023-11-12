import numpy as np
import pulp
import pandas as pd
from itertools import accumulate
import operator

Data = pd.read_excel("/Users/kunwoosmac/Desktop/2023_Spring/MATH 380/MATH380_Project_Data.xlsx")

# 2D Decision variable
COURSE_NAME = Data["MMAE"][:22]
COURSE = list(range(22)) # 수업 종류 22
TIMESLOT = list(range(30)) # 타임슬롯 6 x 5 30개
#print(TIMESLOT)
choices = pulp.LpVariable.dicts("Choice", (COURSE, TIMESLOT), lowBound = 0, upBound = 1, cat= "Binary") # Course 가 Timeslot에 있는지 있으면 1 없으면 0
# print(choices.keys())
lecture_temp = pulp.LpVariable.dicts("temp_course", (list(range(22)), list(range(30))), cat = 'Binary')
lab_temp = pulp.LpVariable.dicts("temp_lab", (list(range(22)), list(range(30))), cat = 'Binary')



prob  = pulp.LpProblem( "Best_Schedule", pulp.LpMinimize )

req_courses_name = [[202, 232], [302, 305, 313, 320], [419, 443, 485], [311, 312, 315, 350], [410, 411, 414, 443], [202, 232], [320, 365, 370, 373], [470,476,485]]

req_courses = []
for req_c in req_courses_name:
    temp = []
    for course in req_c:
        temp.append(np.where(COURSE_NAME==course)[0][0])
    req_courses.append(temp)

print(req_courses)

############################################# Constraint 1 ############################################################
"""
수업시간이 (월,수),(화,목),(이론1시간,실험2시간 1번),(이론2시간, 실험2시간),(이론1시간, 실험3시간 2번) 으로 구성됨.

x_ij = 1 이면 x_i(j+6) = 1
연강 불가능한 시간 6교시 
... 쓰기 귀찮아

"""

time_const = Data['Time'][:22] # 정리했던 엑셀파일에서 방법 열의 값을 가져옴

lab = TIMESLOT
for i in range(5, 30, 6):
    lab.remove(i)
# lab.remove(5, 11, 17, 23, 29) # 연강 시작 시간이 가능한 것 - 마지막 교시는 안되니까 제거


TIMESLOT = list(range(30)) # 이유는 모르겠지만 TIMESLOT이 위의 remove에 영향을 받아서 다시 정의함
lab2 = TIMESLOT[:22]

delete_list_lab2 = [4,5,10,11,16,17]
for delete in delete_list_lab2:
    lab2.remove(delete) # 3시간 연강짜리 랩때문에 만듬.


for i in range(len(COURSE)):

    if time_const[i] == "C21":
        prob += pulp.lpSum( [ choices[i][l] for l in range(24) ] ) == 2 # total 2 hours
        prob += pulp.lpSum([choices[i][l] for l in range(24,30)]) == 0
        for j in range(12):
            prob += choices[i][j] - choices[i][j+12] == 0 # MW or TT


    elif time_const[i] == "C11L12":
        prob += pulp.lpSum( [ choices[i][l] for l in range(len(choices[0])) ] ) == 3 # 수업 1번 1시간씩, 랩 1번 2시간
        temp_2_1 = [choices[i][l] for l in range(len(choices[i]))]
        temp_2_2 = [temp_2_1[l] for l in range(1, len(temp_2_1))]
        temp_2_1 = np.array(temp_2_1[:-1]); temp_2_2 = np.array(temp_2_2)
        temp2 = temp_2_1 + temp_2_2
        print(type(np.any(temp2 >= 2)))
        prob += bool(np.any(temp2 >= 2)) == True
        
        

    elif time_const[i] == "C21L12":
        
        # # Lecture
        prob += pulp.lpSum([lecture_temp[i][l] for l in range(24)]) == 2 # 수업 총 2시간
        prob += pulp.lpSum([lecture_temp[i][l] for l in range(24,30)]) == 0
        for j in range(12):
            prob += lecture_temp[i][j] - lecture_temp[i][j+12] == 0 # 수업이 월수 or 화목으로
        
        # # Lab
        prob += pulp.lpSum( [lab_temp[i][l] for l in range(len(lab_temp[i]))] ) == 2
        temp_3_1 = [lab_temp[i][l] for l in range(len(lab_temp[i]))]
        temp_3_2 = [temp_3_1[l] for l in range(1, len(temp_3_1))]

        temp_3_1 = np.array(temp_3_1[:-1]); temp_3_2 = np.array(temp_3_2)
        temp_3 = temp_3_1 + temp_3_2
        prob += bool(np.any(temp_3 >= 2)) == True
        
        for j in range(30):
            prob += lecture_temp[i][j] + lab_temp[i][j] <= 1   # 겹치지 않게
        for j in range(30):
            prob += choices[i][j] == lecture_temp[i][j] + lab_temp[i][j] # choices 에 임시변수 다시 넣기

    
    elif time_const[i] == "C11L23":
        # prob += pulp.lpSum( [ choices[i][l] for l in range(len(choices[0])) ] ) == 7 # 수업 1번 1시간씩, 랩 2번 3시간씩

        # # Lecture
        prob += pulp.lpSum([lecture_temp[i][l] for l in range(30)]) == 1 # 수업 총 1시간
        
        # # Lab
        prob += pulp.lpSum( [lab_temp[i][l] for l in range(12)] ) == 3
        prob += pulp.lpSum( [lab_temp[i][l] for l in range(12,30)] ) == 3
        temp_4_1 = [lab_temp[i][l] for l in range(12)]
        temp_4_2 = [temp_4_1[l] for l in range(1,12)]
        temp_4_3 = [temp_4_1[l] for l in range(2,12)]

        temp_4_1 = np.array(temp_4_1[:-2]); temp_4_2 = np.array(temp_4_2[:-1]); temp_4_3 = np.array(temp_4_3)
        temp_4_front = temp_4_1 + temp_4_2 + temp_4_3

        temp_4_4 = [lab_temp[i][l] for l in range(12,30)]
        temp_4_5 = [temp_4_4[l] for l in range(17)]
        temp_4_6 = [temp_4_4[l] for l in range(16)]

        temp_4_4 = np.array(temp_4_4[:-2]); temp_4_5 = np.array(temp_4_5[:-1]); temp_4_6 = np.array(temp_4_6)
        temp_4_back = temp_4_4 + temp_4_5 + temp_4_6

        prob += bool(np.any(temp_4_front>=3)) == True
        prob += bool(np.any(temp_4_back>=3)) == True
        # prob += (np.count_nonzero(temp_4 == 3)) == 2

        for j in range(12):
            prob += lab_temp[i][j] - lab_temp[i][j+12] == 0
        
        for j in range(30):
            prob += lecture_temp[i][j] + lab_temp[i][j] <= 1   # 겹치지 않게

        for j in range(30):
            prob += choices[i][j] == lecture_temp[i][j] + lab_temp[i][j] # choices 에 임시변수 다시 넣기

    elif time_const[i] == "C12":
        prob += pulp.lpSum( [ choices[i][l] for l in range(len(choices[i])) ] ) == 2 # 수업 1번 1시간씩, 랩 1번 2시간
        temp_5_1 = [choices[i][l] for l in range(len(choices[i]))]
        temp_5_2 = [temp_5_1[l] for l in range(1, len(temp_5_1))]
        temp_5_1 = np.array(temp_5_1[:-1]); temp_5_2 = np.array(temp_5_2)
        temp5 = temp_5_1 + temp_5_2
        prob += bool(np.any(temp5 >= 2)) == True
    
    else:
        print("????")

####################################################################################################



############################################# Constraint 2 ############################################################

# 같은 시간에 열리는 한 과목에 대하여 같은 교수님이 들어가면 안됨
professors = list(set(Data["Professor"][:22]))

for name in Data['Prof_extended'][:22]:
    if type(name) == str:
        professors.append(name)

professors.sort()
print(professors)

# Make an 22 x 18 matrix. Course x Professor
prof_const = np.zeros((22,len(professors)))

for i in range(len(COURSE_NAME)):
    for j in range(len(professors)):
        if Data['Professor'][i] == professors[j]:
            prof_const[i][j] = 1
        if Data["Prof_extended"][i] == professors[j]:
            prof_const[i][j] = 1




for j in TIMESLOT:
    time_conflict_matrix = np.zeros((len(COURSE), len(professors)), dtype = 'object')
    is_time_conflict = np.zeros((len(professors)), dtype = 'object')
    for i in COURSE:
        for k in range(len(professors)):
            time_conflict_matrix[i,k] = choices[i][j] * prof_const[i,k]

    for i in range(time_conflict_matrix.shape[0]):
        is_time_conflict += time_conflict_matrix[i, :]
    
    for i in range(len(is_time_conflict)):
        prob += is_time_conflict[i] <= 1
    
# ########################################################################################################

# ############################################# Constraint 3 #############################################


for set in req_courses:
    for time in TIMESLOT:
        x = np.empty(30, dtype = 'object')
        for course in set: # 만약 0~4가 필수 코스일 때, 키값으로 포문을 돌리면
            dic = choices[course] 
            x += np.array(list(dic.values()))
        prob += bool(np.all(x <= 1)) == True


# #################################################################################################


############################################# Objective Function #############################################

loss = []
for req_c in req_courses:
    req_courses_timeslot=[]
    for course in req_c: 
        req_courses_timeslot.append(list(choices[course].values())) ## row vector 2x30   
    z=[1]       ## add one in beginning 
    for i in range(len(req_courses_timeslot[0])): # column 
        temp=0
        for j in range(len(req_courses_timeslot)): # row 
            temp = temp+req_courses_timeslot[j][i] # column wise sum 
        z.append(temp)
    z.append(1)  ## add one in end 
    z_idx = list(filter(lambda x:z[x]==1,range(len(z)))) # [1,1,1,0,0,1] - > 01235
    
    idx_distance = []
    for i in range(len(z_idx) - 1):                    
        idx_distance.append(z_idx[i+1] - z_idx[i])          # 앞 인덱스 - 뒤 인덱스 - > EX) 01235 - > 1 1 1 2

    loss.append(sum([(k/len(idx_distance))**2 for k in idx_distance]))


prob += pulp.lpSum(loss)

### Solve
prob.solve()

for j in range(22):
    print('\n')
    for i in range(30):
        print(pulp.value(choices[j][i]), end = '  ')


# for j in range(22):
#     print('\n')
#     for i in range(30):
#         print(pulp.value(lab_temp[j][i]), end = '  ')

##### Optimizing Classroom #####

