# coding=utf8
import sys
import json
import io
import copy
from collections import OrderedDict

VERSION = sys.argv[1]

with io.open(f'{VERSION}/input-goal-list.js', 'r', encoding="utf-8") as file:
    goal_list_file = file.read()

with open(f'{VERSION}/include.txt', 'r') as file:
    goals_to_include = file.read().splitlines()
goals_to_include = [goal.lower() for goal in goals_to_include]

with open(f'{VERSION}/exclude.txt', 'r') as file:
    goals_to_exclude = file.read().splitlines()
goals_to_exclude = [goal.lower() for goal in goals_to_exclude]

goal_list_file = goal_list_file.replace('var bingoList = ', '')
goal_list = json.loads(goal_list_file, object_pairs_hook=OrderedDict)

if 'short' in goal_list:
    del goal_list['short']

print(f"Going through goal list ({VERSION}) at '{VERSION}/input-goal-list.js'...")
beginner_goal_list = copy.deepcopy(goal_list)
handled_goals = []
for difficulty, goals in goal_list['normal'].items():
    beginner_goals = []
    if not difficulty.isdigit():
        continue
    for goal in goals:
        goal_name = goal['name'].lower()
        if goal_name in goals_to_include:
            beginner_goals.append(goal)
            handled_goals.append(goal_name)
        elif goal_name.lower() in goals_to_exclude:
            handled_goals.append(goal_name)
        else:
            print(f"! '{goal['name']}' not present in include.txt nor exclude.txt, will be excluded")
    beginner_goal_list['normal'][difficulty] = beginner_goals

print('\nBeginner Goal list completed.')
for goal in goals_to_include:
    if goal not in handled_goals:
        print(f"! Goal to include '{goal}' was not present in the goal list")
print()
for goal in goals_to_exclude:
    if goal not in handled_goals:
        print(f"! Goal to exclude '{goal}' was not present in the goal list")

beginner_goal_list_string = 'var bingoList = ' + json.dumps(beginner_goal_list, indent=4, ensure_ascii=False).encode('utf8').decode()

file_name = f"{VERSION}/output-beginner-goal-list-{VERSION}.js"
with io.open(file_name, 'w', encoding="utf-8") as file:
    file.write(beginner_goal_list_string)
print(f"Beginner goal list was saved at '{file_name}'")
