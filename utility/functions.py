import numpy, json
from bs4 import BeautifulSoup as bs

def getExercises(data, group, tbody):
    tbody = bs(tbody, "lxml")
    rows = tbody.find_all("tr")

    for i in range(len(rows)):
        tds = rows[i].find_all("td")
        ps = tds[0].find_all("p")
        aelements = tds[0].find_all("a")
        exlesson = {}
        for j in range(len(aelements)):
            exnum = ps[j].text
            try:
                color = aelements[j].find_all("span")[0]["class"]
            except Exception as e:
                print(aelements[j].find_all("span")[0])
                print(j)
                print(aelements[j])
                print(aelements)
                print(e)

            if "HW" in exnum:
                if "red" in color:
                    exlesson["E"+exnum.split("HW")[1]] = False
                elif "green" in color:
                    exlesson["E"+exnum.split("HW")[1]] = True
                else:
                    exlesson["E"+exnum.split("HW")[1]] = "https:" + aelements[j]["href"]
            else:
                if "red" in color:
                    exlesson["H"+exnum.split("Yes")[1]] = False
                elif "green" in color:
                    exlesson["H"+exnum.split("Yes")[1]] = True
                else:
                    exlesson["H"+exnum.split("Yes")[1]] = "https:" + aelements[j]["href"]
                    
        exlesson["points"] = tds[1].text.strip()
        data[group]["students"][i]["lessons"].append(exlesson)
    return data

def getUncheckedExercises(group):
    matrix_list = list()
    for student in group["students"]:
        matrix = list()
        lenmax = max([len(lesson) for lesson in student["lessons"]]) - 1
        maxlesson = max([list(lesson) for lesson in student["lessons"]], key=len)
        for lesson in student["lessons"]:
            lst = list()
            for i in range(lenmax):
                if i < len(lesson) - 1:
                    lst.append((list(lesson)[i], lesson[list(lesson)[i]]))
                else:
                    lst.append((maxlesson[i], None))
            matrix.append(lst)
        matrix_list.append(matrix)
    matrix_list = numpy.transpose(matrix_list, (1, 2, 0, 3))

    clean_matrix = []
    for i in matrix_list:
        temp_i = []
        for j in i:
            temp_j = []
            for k in j:
                if k[1] != None:
                    temp_j.append((k[0], k[1]))
            if len(temp_j) > 0:
                temp_i.append(temp_j)
        clean_matrix.append(temp_i)

    result = []
    for lesson in clean_matrix:
        for i in range(len(lesson)):
            append = 0
            for student in lesson[i]:
                if student[1] != False and student[1] != "False" and student[1] != True and student[1] != "True":
                    result.append(student[1])
                    append += 1
            if i % 2 == 0 and append > 1:
                result.append(None)

    return result if len(result) > 0 else None

def getAllPointsForStudent(student):   # Ritorna i punti totali di uno studente
    points = (0, 0)
    for lesson in student["lessons"]:
        points = (
            points[0] + int(lesson["points"].split("/")[0]) if lesson["points"].split("/")[0] != "" else points[0] + 0, 
            points[1] + int(lesson["points"].split("/")[1]))
    return points

def getStatusExercises(group):      
    
    # Ritorna la lista di tutti gli studenti in un gruppo
    # Ogni studente ha una lista di tuple (lezione, numero esercizi non fatti nella lezione)

    with open("data/exercisesNames.json", "r") as f:
        exercisesNames = json.loads(f.read())

    result = []
    for student in group["students"]:
        studentResult = {}
        studentResult["name"] = student["name"]
        if "phone" in student:
            studentResult["phone"] = student["phone"]
        else:
            studentResult["phone"] = student["parentPhone"]
        studentResult["lessons"] = []
        studentResult["points"] = getAllPointsForStudent(student)
        lessonNames = list(exercisesNames.keys())
        
        for i in range(len(student["lessons"])):
            count = 0
            for exercise in student["lessons"][i]:
                if student["lessons"][i][exercise] == False:
                    count += 1
            studentResult["lessons"].append((lessonNames[i], count))
            
        result.append(studentResult)

    return result