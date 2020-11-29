import random
import json

names = []


def add_name():
    in_name = input("Please enter name: ")
    if in_name.strip() != "":
        names.append(in_name)
    else:
        print("Cannot add blank name.")
        add_name()


add_name()

while input("Continue adding names (y/n): ").lower() == 'y':
    add_name()

if len(names) < 2:
    print("Please enter more than one item")
    add_name()

tempnames = names.copy()

pairings = {}
for name in names:
    not_current_name = list(filter(lambda n: n != name, tempnames))
    choice = random.choice(not_current_name)
    tempnames.remove(choice)
    pairings[name] = choice

print(json.dumps(pairings, indent=4, sort_keys=True, separators=(',', ': ')))
