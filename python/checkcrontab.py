import re, sys

# cron syntax "5 5 5 5 5"

# Scripts vars
# Crontab as python list
cron = sys.argv[1]
splitCron = cron.split()
# Cron position
positionDict = {1:"minute", 2:"hour", 3:"day", 4:"month", 5:"day of the week"}
# Months of the year - mapping
monthsOfTheYear = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
# Days of the year - mapping
daysOfTheWeek = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday", 7:"Sunday" }
# Final list we will print out to the user
humanReadableCron = []

# Define the function used to parse each cron argument

def checkMinute(minute):
    minRegex = "^[1-5]?[0-9]$"
    if re.match(minRegex, minute):
        print("at minute "+minute)
        humanReadableCron.append("at minute "+minute)
    else:
        print("Your syntax does not match the min syntax (allowed value : 0-59)")

def checkHour(hour):
    hourRegex = "^(2[0-4]|1[0-9]|[1-9])$"
    if re.match(hourRegex, hour):
        print("past hour "+hour)
        humanReadableCron.append("past hour "+hour)
    else:
        print("Your syntax does not match the hour syntax (allowed value : 0-24)")

def checkDay(day):
    dayRegex = "^(3[01]|[12][0-9]|[1-9])$"
    if re.match(dayRegex, day):
        print("on day-of-month "+day)
        humanReadableCron.append("on day-of-month "+day)
    else:
        print("Your syntax does not match the day syntax (allowed value : 0-31)")

def checkMonth(month):
    monthRegex = "^(0[0-2]|[1-9])$"
    if re.match(monthRegex, month):
        print("in "+monthsOfTheYear[int(month)])
        humanReadableCron.append("in "+monthsOfTheYear[int(month)])
    else:
        print("Your syntax does not match the month syntax (allowed value : 0-12)")

def checkWeekDay(weekday):
    weekdayRegex = "([0-6])"
    if re.match(weekdayRegex, weekday):
        print("on "+daysOfTheWeek[int(weekday)])
        humanReadableCron.append("on "+daysOfTheWeek[int(weekday)])
    else:
        print("Your syntax does not match the weekday syntax (allowed value : 0-6)")

# List with all of ours functions
checks = [checkMinute, checkHour, checkDay,checkMonth,checkWeekDay]

############### OLD #################
#         REPLACED BY ZIP           #
#####################################

def checkParam(position, param):
    if param != "*":
        if position == 1:
            checkMinute(param)
        if position == 2:
            checkHour(param)
        if position == 3:
            checkDay(param)
        if position == 4:
            checkMonth(param)
        if position == 5:
            checkWeekDay(param)
    else:
        s="s" if position < 5 else ""
        print("every " + positionDict[position]+s)
        humanReadableCron.insert(position, "every " + positionDict[position]+s)

############# END OLD ###############

def checkParams(cronlist):
    if len(cronlist) != 5:
        print("Please check your crontab synxtax, you have "+ len(cronlist)+" instead of 5 params")
        return False
    print("Your crontab syntax got 5 params")

    for function, element in zip(checks, splitCron):
        function(element)

checkParams(splitCron)

print(humanReadableCron)

# def listToSentence(mylist):
#     sentence = ""
#     minutes = re.sub('\D', '', str(mylist[0])) if int(re.sub('\D', '', str(mylist[0]))) >= 10 else "0"+re.sub('\D', '', str(mylist[0]))
#     # 5 * * * *
#     if "every" not in mylist[0] and "every" in mylist[1] and "every" in mylist[2] and "every" in mylist[3] and "every" in mylist[4]:
#         sentence += "At minute "+minutes+"."
#     # 5 5 * * *
#     if "every" not in mylist[0] and "every" not in mylist[1] and "every" in mylist[2] and "every" in mylist[3] and "every" in mylist[4]:
#         sentence += "At "+re.sub('\D', '', str(mylist[1]))+":"+minutes+"."
#     # 5 5 5 * *
#     if "every" not in mylist[0] and "every" not in mylist[1] and "every" not in mylist[2] and "every" in mylist[3] and "every" in mylist[4]:
#         sentence += "At "+re.sub('\D', '', str(mylist[1]))+":"+minutes+" "+mylist[2]
#     # 5 5 5 5 *
#     if "every" not in mylist[0] and "every" not in mylist[1] and "every" not in mylist[2] and "every" not in mylist[3] and "every" in mylist[4]:
#         sentence += "At "+re.sub('\D', '', str(mylist[1]))+":"+minutes+" "+mylist[2]+" "+mylist[3]
#     # 5 5 5 5 5
#     if "every" not in mylist[0] and "every" not in mylist[1] and "every" not in mylist[2] and "every" not in mylist[3] and "every" not in mylist[4]:
#         sentence += "At "+re.sub('\D', '', str(mylist[1]))+":"+minutes+" "+mylist[2]+" and "+mylist[4]+" "+mylist[3]

#     print(sentence)
# listToSentence(humanReadableCron)
