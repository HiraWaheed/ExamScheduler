##with actual dataset
import pandas as pd
import copy
from random import *
class ExamScheduler:
    def __init__(self, weeks):
        self.bestSolution = []
        self.bestCost = 0
        self.file_courses = "courses1.csv"
        self.file_teachers = "teachers1.csv"
        self.file_rooms = "rooms1.csv"
        self.file_studentNames = "studentNames1.csv"
        self.file_studentCourses = "studentCourse1.csv"
        # reading data from excel file
        self.courses = pd.read_csv(self.file_courses, header=None)
        self.teachers = pd.read_csv(self.file_teachers, header=None)
        self.rooms = pd.read_csv(self.file_rooms, header=None)
        self.studentNames = pd.read_csv(self.file_studentNames, header=None)
        self.studentCourses = pd.read_csv(self.file_studentCourses)
        self.CoursesList = {}
        self.RoomsList = {}
        self.TeachersList = self.teachers.values.tolist()
        self.StudentNamesList = self.studentNames.values.tolist()
        self.CoursewiseStudentsList = {}  # store students(values) against courses(key)
        self.StudentsCoursesList = {}  # store courses list of each student
        if weeks == 2:
            self.dayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                            "Monday1", "Tuesday1", "Wednesday1", "Thursday1","Friday1"]

        else:
            self.dayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                            "Monday1", "Tuesday1", "Wednesday1", "Thursday1", "Friday1",
                            "Monday2", "Tuesday2","Wednesday2","Thursday2","Friday2"]

        self.timeListMontoThur = ["09:00-10:00", "10:30-11:30", "12:00-1:00", "01:30-02:30", "02:45-03:45", "04:00-05:00"]
        self.timeListFri = ["09:00-10:00", "10:30-11:30", "12:00-1:00", "02:00-03:00", "03:10-04:10", "04:15-05:15"]
        # converting read data into templist
        self.cList = self.courses.values.tolist()
        self.rList = self.rooms.values.tolist()
        self.scList = self.studentCourses.values.tolist()
    def dataReading(self):
        # entering in dictionary
        tempT = []
        for list in self.TeachersList:
            mystring = ''.join(map(str, list))#converting Teachers list of lists into list of strings
            tempT.append(mystring)
        self.TeachersList = tempT.copy()
        for i in range(len(self.cList)):
            for j in range(len(self.cList[i]) - 1):
                self.CoursesList[self.cList[i][j]] = self.cList[i][j + 1]

        for i in range(len(self.rList)):
            for j in range(len(self.rList[i]) - 1):
                self.RoomsList[self.rList[i][j]] = self.rList[i][j + 1]

        for i in range(len(self.cList)):
            temp = []
            for j in range(len(self.scList)):
             if self.scList[j][2] == self.cList[i][0]:
                temp.append(self.scList[j][1])
                self.CoursewiseStudentsList[self.cList[i][0]] = temp
        for i in range(len(self.scList)):
            temp1 = []
            for j in range(len(self.scList)):
                if self.scList[i][1] == self.scList[j][1]:
                    if self.scList[j][2] in self.CoursesList.keys():
                        courseCode = self.scList[j][2]
                        temp1.append(courseCode)
                    self.StudentsCoursesList[self.scList[i][1]] = temp1

    def generateRandomSolution(self):
        print("\t --------Generating random solution------->")
        courseNumbers = []
        tempList = self.cList.copy()
        random_solution_list = []
        for i in range(len(self.courses)):
            random_course = randint(0, len(self.courses) - 1)
            while random_course in courseNumbers:  # value repeated
                random_course = randint(0, len(self.courses) - 1)
            courseNumbers.append(random_course)
            course_name = tempList[random_course][0]  # cs121
            random_teacher = randint(0, len(self.TeachersList) - 1)
            random_day = randint(0, len(self.dayList) - 1)
            random_room = randint(0, len(self.rList) - 1)
            if self.dayList[random_day] == "Friday" or self.dayList[random_day] == "Friday1" or self.dayList[
                random_day] == "Friday2":
                random_time = randint(0, len(self.timeListFri) - 1)
                random_solution_list.append(
                    [self.cList[random_course][0], self.TeachersList[random_teacher], self.dayList[random_day],
                     self.rList[random_room][0], self.timeListFri[random_time]])
            else:
                random_time = randint(0, len(self.timeListMontoThur) - 1)
                random_solution_list.append(
                    [self.cList[random_course][0], self.TeachersList[random_teacher], self.dayList[random_day],
                     self.rList[random_room][0], self.timeListMontoThur[random_time]])
        # print("\tDisplaying random solution of scheduled exams")
        for exam in random_solution_list:
            print(exam)
        self.bestSolution = random_solution_list
        return random_solution_list
    #Optimization functions
    def checkCourseNotScheduled(self, solution):
        counter = 0
        for i in range(len(solution)):
            if solution[i][0] not in self.CoursesList.keys():
                print(solution[i][0], "not scheduled")
                counter += 1
        # print("\tCourses not scheduled", counter)
        return counter

    def checkStudentClashes(self, solution):
        stdClashDict = {}
        for student in self.StudentsCoursesList.keys():
            sCount = 0
            for course in self.StudentsCoursesList[student]:
                for i in range(len(solution)):
                    if course == solution[i][0]:
                        examDay = solution[i][2]
                        examTime = solution[i][4]
                        for j in range(len(solution)):
                            if solution[j][2] == examDay and solution[j][4] == examTime:
                                course2 = solution[j][0]
                                if course2 != course:
                                    if course2 in self.StudentsCoursesList[student]:
                                        # print("       !!!!!found exam clash!!!!! of ",student,"  ",course," with  ",course2)
                                        sCount = sCount + 1
                                        stdClashDict[student] = sCount
        # print("Clash list",stdClashDict)
        no_StudentHavingClashes = len(stdClashDict)
        # print("\tNo of Student having clashes", no_StudentHavingClashes)
        return no_StudentHavingClashes

    def checkTeacherClashes(self, solution):
        teacherClashDict = {}
        teacherClashDict1 = {}
        for exam in solution:
            teacher = exam[1]
            tAtCount = 0
            tInRowCount = 0
            examDay = exam[2]
            examTime = exam[4]
            for exam2 in solution:  # check if that teacher has clash with another exam at same day&time
                if exam2[1] == teacher:
                    if exam != exam2:
                        if exam2[2] == examDay:  # two invigilations at time
                            examTime2 = exam2[4]
                            if examTime2 == examTime:
                                # print("       !!!!!found invigilation clash!!!!! of ", teacher, "  ", exam[0], " with ", exam2[0])
                                tAtCount = tAtCount + 1
                                teacherClashDict[teacher] = tAtCount + 1
                            else:
                                t1 = examTime  # to check exams in a row
                                t2 = examTime2
                                if examDay == "Friday" or examDay == "Friday1" or examDay == "Friday2":
                                    if examTime in self.timeListFri:
                                        index1 = self.timeListFri.index(examTime)
                                    else:
                                        index1 = -1
                                    if examTime2 in self.timeListFri:
                                        index2 = self.timeListFri.index(examTime2)
                                    else:
                                        index2 = -1
                                    if abs(index1 - index2) == 1:
                                        # print("       !!!!!found two invigilations in row !!!!! of ", teacher, "  ",exam[0], " with ", exam2[0])
                                        tInRowCount = tInRowCount + 1
                                        teacherClashDict1[teacher] = tInRowCount + 1
                                else:
                                    if examTime in self.timeListMontoThur:
                                        index1 = self.timeListMontoThur.index(examTime)
                                    else:
                                        index1 = -1
                                    if examTime2 in self.timeListMontoThur:
                                        index2 = self.timeListMontoThur.index(examTime2)
                                    else:
                                        index2 = -1
                                    if abs(index1 - index2) == 1:
                                        # print("       !!!!!found two invigilations in row !!!!! of ", teacher, "  ",exam[0], " with ", exam2[0])
                                        tInRowCount = tInRowCount + 1
                                        teacherClashDict1[teacher] = tInRowCount + 1

        # print("\tSame time clash", teacherClashDict, len(teacherClashDict))
        # print("\tIn a row time clash", teacherClashDict1, len(teacherClashDict1))
        return len(teacherClashDict) + len(teacherClashDict1)

    def getCostValue(self, solution):
        print("\t ....Calculating Cost Value....")
        courses_not_scheduled = self.checkCourseNotScheduled(solution)
        student_clashes = self.checkStudentClashes(solution)
        teacher_clashes = self.checkTeacherClashes(solution)
        # consective_exams = self.checkConsectiveExams(solution)
        value = courses_not_scheduled + student_clashes + teacher_clashes
        # value=courses_schedule+student_clashes*10+teacher_clashes*10+consective_exams*0.5
        print("\tNumber of clashes ", value)
        return value

    def neighbouringSolution(self, csolution):
        print("\t ....Generating a neighbouring solution....")
        random_no = randint(0, len(csolution) - 1)
        random_dayNo = randint(0, len(self.dayList) - 1)
        random_day = self.dayList[random_dayNo]
        csolution[random_no][2] = random_day  # update day of exam
        return csolution

    def simulatedAnnealing(self):
        print("\t----Simulated Annealing Local Search Algorithm for minimizing cost------->")
        temperature = 500
        rate = 0.5
        currentSol = copy.deepcopy(self.bestSolution)
        currentCost = self.bestCost
        if self.bestCost == 0:
            print("\n\n\t\tOptimal solution found")
        else:
            while temperature > 0:
                newSol = copy.deepcopy(self.neighbouringSolution(currentSol))
                newCost = self.getCostValue(newSol)
                if newCost == 0:  # number of attacks are none
                    self.bestCost = newCost
                    self.bestSolution = copy.deepcopy(newSol)
                    print("\n\n\t\tOptimal solution found")
                    break
                if newCost < currentCost:  # better solution
                    self.bestSolution = copy.deepcopy(newSol)
                    self.bestCost = newCost
                    currentSol = copy.deepcopy(newSol)
                    currentCost = newCost
                elif (2.71828182 ** (
                        currentCost - newCost) / temperature) > 0.5:  # calculating probability of bad moves
                    currentSol = copy.deepcopy(newSol)
                    currentCost = newCost
                temperature = temperature - rate
                rate += 0.5

        print("\n\t\tOptimal cost is ", self.bestCost, " & SOLUTION is:\n")
        for exam in self.bestSolution:
            print(exam)

week = 2
while True:
    option = int(input("Select from following:\n1.Two weeks schedule\n2.Three weeks schedule\n"))
    if option == 1:
        week = 2
        break
    elif option == 2:
        week = 3
        break
    else:
        continue

e = ExamScheduler(week)
e.dataReading()
print("HARD CONSTRAINT: Exam not held on weekends")
print("HARD CONSTRAINT: Exam will be held between 9AM to 5PM")
print("HARD CONSTRAINT: An exam will be scheduled for each course")
print("HARD CONSTRAINT: A student cannot give more than 1 exam at a time")
print("HARD CONSTRAINT: A teacher cannot invigilate two exams at the same time.A teacher cannot invigilate two exams in a row.")
print("SOFT CONSTRAINT: All students and teachers shall be given a break on Friday from 1-2.")

solution = e.generateRandomSolution()
cost = e.getCostValue(solution)
e.bestCost = cost
e.simulatedAnnealing()

