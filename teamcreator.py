import itertools
import pprint

with open("times.txt", "r") as f:
    times = []
    for line in f:
        temp = line.split()
        temp[1] = int(temp[1][2:4]) * 60 + int(temp[1][5:])
        temp[2] = int(temp[2][2:4]) * 60 + int(temp[2][5:])
        times.append(temp)

class Team:
    def __init__(self, members, expected_pb, expected_average):
        self.members = members
        self.pbs, self.averages = self.getSums()
        self.expected_pb = expected_pb
        self.expected_average = expected_average
        self.ranking = abs(self.pbs - self.expected_pb) + abs(self.averages - self.expected_average)
    def __lt__(self, other):
        return (abs(self.pbs - self.expected_pb) + abs(self.averages - self.expected_average)
               < abs(other.pbs - other.expected_pb) + abs(other.averages - other.expected_average))
    def getSums(self):
        pbs = 0
        avgs = 0
        for member in self.members:
            pbs += member[1]
            avgs += member[2]
        return pbs,avgs
    def getMembers(self):
        return self.members
    def __eq__(self, other):
        return (abs(self.pbs - self.expected_pb) + abs(self.averages - self.expected_average)
               == abs(other.pbs - other.expected_pb) + abs(other.averages - other.expected_average))

def has_a_common_member(t1, t2):
    for t in t1:
        if t in t2:
            return False
    return True

number_of_players = len(times)
number_of_teams = 4

total_pb = 0
total_average = 0
for time in times:
    total_pb += time[1]
    total_average += time[2]

teams = itertools.combinations(times, len(times)// number_of_teams)
cteams = []
for team in teams:
    cteams.append(Team(team, total_pb/number_of_teams, total_average/number_of_teams))
cteams.sort()

pteams = []

for team in cteams:
    pteams.append(team.members)

flag = False
fullteams = []
candidates = []
counter = 0
for team in pteams:
    counter += 1
    if flag:
        break
    for candidate in candidates:
        if has_a_common_member(team, candidate):
            if len(candidate + team) == number_of_players:
                fullteams.append(candidate+team)
                if len(fullteams) >= 1:
                    flag = True
                    break
            candidates.append(candidate + team)
    candidates.append(team)

with open('teams.txt', 'w') as f:
    for fullteam in fullteams:
        lines = [""] * (number_of_players//number_of_teams)
        separator = "\t"
        for i in range(len(fullteam)):
            strings = [str(integer) for integer in fullteam[i]]
            strings[1] = "0:" + str(int(strings[1])//60) + ":" + str(int(strings[1])%60)
            strings[2] = "0:" + str(int(strings[2])//60) + ":" + str(int(strings[2])%60)
            lines[i % (number_of_players//number_of_teams)] += separator.join(strings) + "\t"
        for line in lines:
            f.write(line + "\n")
        f.write("\n\n")

print("done")
