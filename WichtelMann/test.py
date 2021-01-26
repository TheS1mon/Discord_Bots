birthdayList= [[],[]]
with open("birthdays.txt", 'r') as file:
    lines = file.readlines()
    print(lines)
    for line in lines:
        line = line.replace("\n", "")
        name, birthday = line.split(':')
        birthdayList[0].append(name)
        birthdayList[1].append(birthday)
    print(birthdayList)