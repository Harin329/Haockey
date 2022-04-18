import csv
import itertools
from operator import itemgetter

userList = ['Angelo', 'Alessio', 'Harin', 'Parsa', 'Quin', 'Yashar']

myList = list(itertools.permutations(userList))

def make_day(num_teams, day):
    # using circle algorithm, https://en.wikipedia.org/wiki/Round-robin_tournament#Scheduling_algorithm
    assert not num_teams % 2, "Number of teams must be even!"
    # generate list of teams
    lst = list(range(1, num_teams + 1))
    # rotate
    day %= (num_teams - 1)  # clip to 0 .. num_teams - 2
    if day:                 # if day == 0, no rotation is needed (and using -0 as list index will cause problems)
        lst = lst[:1] + lst[-day:] + lst[1:-day]
    # pair off - zip the first half against the second half reversed
    half = num_teams // 2
    return list(zip(lst[:half], lst[half:][::-1]))

def make_schedule(num_teams):
    """
    Produce a double round-robin schedule
    """
    # number of teams must be even
    if num_teams % 2:
        num_teams += 1  # add a dummy team for padding

    # build first round-robin
    schedule = [make_day(num_teams, day) for day in range(num_teams - 1)]
    # generate second round-robin by swapping home,away teams
    swapped = [[(away, home) for home, away in day] for day in schedule]

    return schedule + swapped

schedule = make_schedule(6)
# print(schedule)
scheduleLen = len(schedule)

angeloFinal = 0
alessioFinal = 0
harinFinal = 0
parsaFinal = 0
quinFinal = 0
yasharFinal = 0

for userList in myList:
    print(schedule)

    week = 0

    angelo = 0
    alessio = 0
    harin = 0
    parsa = 0
    quin = 0
    yashar = 0

    print("New Scenario")
    with open('scores.csv', mode ='r') as predictionFile:
        predictionReader = csv.reader(predictionFile)
        for prediction in predictionReader:
            if (prediction[0] != "Angelo"):
                # Matchday
                print("New Matchday")
                # print(schedule[week])

                # Matches
                for match in schedule[week]:
                    # print(str(match[0] - 1) + " vs " + str(match[1] - 1))
                    print(userList[match[0] - 1] + " vs " + userList[match[1] - 1])
                    if (userList[match[0] - 1] == "Angelo"):
                        p0 = "Angelo"
                        p0Score = prediction[0]
                    elif (userList[match[0] - 1] == "Alessio"):
                        p0 = "Alessio"
                        p0Score = prediction[1]
                    elif (userList[match[0] - 1] == "Harin"):
                        p0 = "Harin"
                        p0Score = prediction[2]
                    elif (userList[match[0] - 1] == "Parsa"):
                        p0 = "Parsa"
                        p0Score = prediction[3]
                    elif (userList[match[0] - 1] == "Quin"):
                        p0 = "Quin"
                        p0Score = prediction[4]
                    elif (userList[match[0] - 1] == "Yashar"):
                        p0 = "Yashar"
                        p0Score = prediction[5]

                    if (userList[match[1] - 1] == "Angelo"):
                        p1 = "Angelo"
                        p1Score = prediction[0]
                    elif (userList[match[1] - 1] == "Alessio"):
                        p1 = "Alessio"
                        p1Score = prediction[1]
                    elif (userList[match[1] - 1] == "Harin"):
                        p1 = "Harin"
                        p1Score = prediction[2]
                    elif (userList[match[1] - 1] == "Parsa"):
                        p1 = "Parsa"
                        p1Score = prediction[3]
                    elif (userList[match[1] - 1] == "Quin"):
                        p1 = "Quin"
                        p1Score = prediction[4]
                    elif (userList[match[1] - 1] == "Yashar"):
                        p1 = "Yashar"
                        p1Score = prediction[5]

                    if (p0Score > p1Score):
                        print(p0 + " wins!")
                        if (p0 == "Angelo"):
                            angelo += 1
                        elif (p0 == "Alessio"):
                            alessio += 1
                        elif (p0 == "Harin"):
                            harin += 1
                        elif (p0 == "Parsa"):
                            parsa += 1
                        elif (p0 == "Quin"):
                            quin += 1
                        elif (p0 == "Yashar"):
                            yashar += 1
                    elif (p0Score < p1Score):
                        print(p1 + " wins!")
                        if (p1 == "Angelo"):
                            angelo += 1
                        elif (p1 == "Alessio"):
                            alessio += 1
                        elif (p1 == "Harin"):
                            harin += 1
                        elif (p1 == "Parsa"):
                            parsa += 1
                        elif (p1 == "Quin"):
                            quin += 1
                        elif (p1 == "Yashar"):
                            yashar += 1

                week += 1
                if (week == scheduleLen):
                    week = 0

    test = [("angelo", angelo), ("alessio", alessio), ("harin", harin), ("parsa", parsa), ("quin", quin), ("yashar", yashar)]
    sortedList = sorted(test, key=itemgetter(1), reverse=True)

    winner = sortedList[0]

    print(winner[0] + " wins!")
    if (winner[0] == "angelo"):
        angeloFinal += 1
    elif (winner[0] == "alessio"):
        alessioFinal += 1
    elif (winner[0] == "harin"):
        harinFinal += 1
    elif (winner[0] == "parsa"):
        parsaFinal += 1
    elif (winner[0] == "quin"):
        quinFinal += 1
    elif (winner[0] == "yashar"):
        yasharFinal += 1

print("Angelo: " + str(angeloFinal))
print("Alessio: " + str(alessioFinal))
print("Harin: " + str(harinFinal))
print("Parsa: " + str(parsaFinal))
print("Quin: " + str(quinFinal))
print("Yashar: " + str(yasharFinal))