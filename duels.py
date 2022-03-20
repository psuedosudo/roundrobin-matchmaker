#!/bin/python
from os import system, name
from datetime import datetime
from pathlib import Path
import sys

# Class object for storing player metrics
class Combatant:
    def __init__(self, name, level, index):
        self.name = name
        self.level = level

        # theres probably a better way to do this, but I'm just keeping the list position
        # as an atribute in the object so I can reference it for cross referencing for
        # wins and loss calculations with other combatants
        self.index = index

        # Later, the list of users is iterated on, and this value becomes a list of 0's
        # the size of len(adversaries). The position is referential to the index of the 
        # corrisponding combatant
        self.record = []

        # First position is peak, second position is current win streak
        self.streak = [0, 0]

def matchmaking(players):
# stolen from https://stackoverflow.com/questions/11245746/league-fixture-generator-in-python/11246261#11246261
# I tbh don't understand this too much, but it places round robin matchmaking into sets of
# lists with tuples. We iterate through the data sets and refresh them when done.
    players = list(range(0, len(players)))
    if (len(players) % 2) != 0:
        players.append('Skip')
    n = len(players)
    matchs = []
    fixtures = []
    return_matchs = []
    for fixture in range(1, n):
        for i in range(int(n/2)):
            matchs.append((players[i], players[n - 1 - i]))
            return_matchs.append((players[n - 1 - i], players[i]))
        players.insert(1, players.pop())
        fixtures.insert(int(len(fixtures)/2), matchs)
        fixtures.append(return_matchs)
    return fixtures

# Prints the results table.
def results():
    clear()
    print("\n"+"="*75)
    for x in adversaries:
        wins = 0
        losses = 0
        for y in adversaries:
            losses += y.record[x.index]
        for i in x.record:
            wins += i
        print("\n%s[%s] - Wins: %s, Losses: %s, Winstreak: Total %s Peak %s" % 
                (x.name, x.level, wins, losses, x.streak[1], x.streak[0]))
        for y in adversaries:
            if x is not y:
                print("\t%s[%s] - Wins: %s  Losses: %s" % 
                        (y.name, y.level, x.record[y.index], y.record[x.index]))
    print("\n" + "=" * 75 + "\n")

# Update statistics
def update(i, x, y):
    adversaries[i[x]].record[adversaries[i[y]].index] += 1
    adversaries[i[x]].streak[1] += 1
    adversaries[i[y]].streak[1] = 0
    if adversaries[i[x]].streak[1] > adversaries[i[x]].streak[0]:
        adversaries[i[x]].streak[0] = adversaries[i[x]].streak[1] 

# Generic console clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# Changes the output of stdout to write results to file
def saveresults():
    results()
    original_stdout = sys.stdout # Save a reference to the original standard output
    file_path = Path("metrics_" + datetime.now().strftime("%Y.%m.%d-%H:%M:%S") + ".txt")
    file_path.touch(exist_ok=True)
    with open(file_path, 'w+') as f:
        sys.stdout = f # Change the standard output to the file we created.
        results()
        sys.stdout = original_stdout # Reset the standard output to its original value

# List to hold Combatant objects.
adversaries = []

clear()
print("\nEnter adversaries. Enter a blank combatant name to continue.")

# Combatants Input
index = 0
while True:
    name = input("\nEnter Combatant: ")
    if name == "":
        break
    level = input("Enter Level: ")
    adversaries.append(Combatant(name, level, index))
    index += 1

# Establish win metrics table for each user object
for i in adversaries:
    i.record = [0] * len(adversaries)

# Main Loop
while True:
    fixtures = matchmaking(adversaries)
    end = 0
    for fixture in fixtures:
        for i in fixture:
            try:
                # if the list of combatants is too long, don't flood the screen.
                # might make a more compact results function output later.
                if len(adversaries) < 8:
                    results()
                else:
                    clear()
                print("%s[%s] (Streak: %s) VS %s[%s] (Streak: %s)" %  
                    (adversaries[i[0]].name, adversaries[i[0]].level, adversaries[i[0]].streak[1],
                    adversaries[i[1]].name, adversaries[i[1]].level, adversaries[i[1]].streak[1]))

                result = input("Results? %s(1), %s(2), Draw(3), End(4): " %
                    (adversaries[i[0]].name, adversaries[i[1]].name))

                match result:
                    case "1":
                        update(i, 0, 1)
                    case "2":
                        update(i, 1, 0)
                    case "3":
                        pass
                    case "4":
                        end = 1
                        break            
            except Exception as e:
                # pass
                print(e)
        if end == 1:
            break
    if end == 1:
        break

saveresults()

