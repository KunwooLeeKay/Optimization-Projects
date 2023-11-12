import numpy as np
import pulp
import pandas as pd

Data = pd.read_excel("/Users/kunwoosmac/Desktop/2023_Spring/MATH 380/MATH380_Project_Data.xlsx")

# 2D Decision variable
COURSE_NAME = Data["MMAE"][:22]
COURSE = list(range(22)) # 수업 종류 22
TIMESLOT = list(range(30)) # 타임슬롯 6 x 5 30개
#print(TIMESLOT)
choices = pulp.LpVariable.dicts("Choice", (COURSE, TIMESLOT), lowBound = 0, upBound = 1, cat= "Binary") # Course 가 Timeslot에 있는지 있으면 1 없으면 0
# print(choices.keys())
print(choices)
    
prob  = pulp.LpProblem( "Best Schedule", pulp.LpMinimize )

req_courses_name = [[202, 232], [302, 305, 313, 320], [419, 443, 485], [311, 312, 315, 350], [410, 411, 414, 443], [202, 232], [320, 365, 370, 373], [470,476,485]]
req_courses = []
for set in req_courses_name:
    temp = []
    for course in set:
        temp.append(np.where(COURSE_NAME==course)[0][0])
    req_courses.append(temp)


############################################# Constraint 1 ############################################################
"""
수업시간이 (월,수),(화,목),(이론1시간,실험2시간 1번),(이론2시간, 실험2시간),(이론1시간, 실험3시간 2번) 으로 구성됨.

x_ij = 1 이면 x_i(j+6) = 1
연강 불가능한 시간 6교시 
... 쓰기 귀찮아

"""

time_const = Data['Time'][:22] # 정리했던 엑셀파일에서 방법 열의 값을 가져옴
print(time_const)

lab = TIMESLOT
for i in range(5, 30, 6):
    lab.remove(i)
# lab.remove(5, 11, 17, 23, 29) # 연강 시작 시간이 가능한 것 - 마지막 교시는 안되니까 제거


TIMESLOT = list(range(30)) # 이유는 모르겠지만 TIMESLOT이 위의 remove에 영향을 받아서 다시 정의함
lab2 = TIMESLOT[:22]

delete_list_lab2 = [4,5,10,11,16,17]
for delete in delete_list_lab2:
    lab2.remove(delete) # 3시간 연강짜리 랩때문에 만듬.

#print(len(COURSE), len(TIMESLOT), len(time_const))

for i in range(len(COURSE)):

    if time_const[i] == "C21":
        prob += pulp.lpSum( [ choices[i][l] for l in range(24) ] ) == 2 # 수업 총 2시간
        prob += pulp.lpSum([choices[i][l] for l in range(24,30)]) ==0 
        for j in range(12):
            prob += choices[i][j] - choices[i][j+12] == 0 # 수업이 월수 or 화목으로
            


    if time_const[i] == "C11L12":
        prob += pulp.lpSum( [ choices[i][l] for l in range(len(choices[0])) ] ) == 3 # 수업 1번 1시간씩, 랩 1번 2시간

        a = [choices[i][l] for l in range(len(choices[i]))]
        b = [a[l] for l in range(1, len(a))]
        a = np.array(a[:-1]); b = np.array(b)
        c = a + b
        prob += c.any() >= 2
        # for j in range(23):
        #     prob += (choices[i][j] - choices[i][j+1])*(choices[i][j+2]-choices[i][j+3])*(choices[i][j+4]-choices[i][j+5])*(choices[i][j+6]-choices[i][j+7])==0 

        # a = np.empty(29, dtype = 'object')
        # for l in range(29):
        #     a[l] = choices[i][l] - choices[i][l+1]
        # prob += pulp.lpDot([choices[i][j] - choices[i][j+1] for j in range(29)], [choices[i][j] - choices[i][j+1] for j in range(29)]) == 4
        # for j in range(28):
        #     prob += choices[i][j] + choices[i][j+1] == 2 
        #     prob += choices[i][j] + choices[i][j+1] + choices[i][j+2] ==3
        # for k in lab:
        #     prob += pulp.lpSum([choices[i][l] for l in [k, k+1]]) == 2 # 랩 2시간씩 연강으로

    if time_const[i] == "C21L12":
        prob += pulp.lpSum( [ choices[i][l] for l in range(len(choices[0])) ] ) == 4 # 수업 2번 1시간씩, 랩 1번 2시간씩
        # a = [choices[i][j] - choices[i][j+1] for j in range(29)]
        for j in range(12):
            prob += choices[i][j] - choices[i][j+12] == 0 # 수업이 월수 or 화목으로
        # flag = False
        # for j in range(len(a)-2):
        #     if a[j] == -1:
        #         if a[j+1] == 0:
        #             if a[j+2] == 1:
        #                 flag = True
        # prob += flag == True
        # for k in range(12):
        #     prob += pulp.lpSum([choices[i][l] for l in [k, k+6]]) == 2 # 수업이 월수 or 화목으로
        # for m in lab:
        #     prob += pulp.lpSum([choices[i][l] for l in [m, m+1]]) == 2 # 랩 2시간씩 연강으로 
    
    if time_const[i] == "C11L23":
        prob += pulp.lpSum( [ choices[i][l] for l in range(len(choices[0])) ] ) == 7 # 수업 1번 1시간씩, 랩 2번 3시간씩
        # for k in lab2:
        #     prob += pulp.lpSum([choices[i][l] for l in [k, k+1, k+2, k+6, k+7, k+8]]) == 6  # 랩이 3시간 연강으로, 하루 띄고 있도록 정의

####################################################################################################



############################################# Constraint 2 ############################################################

# # 같은 시간에 열리는 한 과목에 대하여 같은 교수님이 들어가면 안됨
# professors = list(set(Data["Professor"][:22]))

# for name in Data['Prof_extended'][:22]:
#     if type(name) == str:
#         professors.append(name)

# professors.sort()

# # Make an 22 x 17 matrix. Time x Course x Professor
# prof_const = np.zeros((22,17))

# for i in range(len(COURSE_NAME)):
#     for j in range(17):
#         if Data['Professor'][i] == professors[j]:
#             prof_const[i][j] = 1
#         if Data["Prof_extended"][i] == professors[j]:
#             prof_const[i][j] = 1


# for time in TIMESLOT:
#     temp = list(choices.values())
#     for i, dic in enumerate(temp): # course를 한줄씩 가져옴
#         prob += pulp.lpSum(pulp.lpDot(list(dic.values())[time], prof_const[i,:])) <= 1

#         # is_class = (list(dic.values())[time]) # 이렇게 하면 특정 수업에 대해 수업이 time 교시에 열리는지 가져올 수 있음.
#         # okay += prof_const[i, :] * is_class # 열리는 수업에 대해서 교수님이 겹치면 안됨

# ####################################################################################################

# ############################################# Constraint 3 #############################################


# for set in req_courses:
#     for time in TIMESLOT:
#         x = np.empty(30, dtype = 'object')
#         for course in set: # 만약 0~4가 필수 코스일 때, 키값으로 포문을 돌리면
#             dic = choices[course] 
#             x += np.array(list(dic.values()))
#         prob += x.all() <= 1


# #################################################################################################

############################################# Objective Function #############################################

loss = []
for set in req_courses:
    req_courses_timeslot=[]
    for course in set: 
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

##### Optimizing Classroom #####

