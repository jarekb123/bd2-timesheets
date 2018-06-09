from random import randint

file = open("abc.txt", "w")

id = 1

for employee_id in range(1, 101):
    for month in range(2, 6):
        file.write("insert into summarize (`id`, `employee_id`, `month`, `year`, `salary`) values (" + str(id) +
                   ", " + str(employee_id) + ", " + str(month) + ", 2018," + str(randint(5000, 15000)) + ");\n")
        id += 1


file.close()

