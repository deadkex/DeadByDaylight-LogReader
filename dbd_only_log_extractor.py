import os
path = os.path.expandvars(r'%LOCALAPPDATA%')


with open(path + '\\DeadByDaylight\\Saved\\Logs\\DeadByDaylight.log', 'r', encoding='utf-8') as file:
    try:
        x = file.readlines()
    except:
        print("Cannot read file")

reader = ""
for line in x:
    if "LogCustomization: -->" in line or "Sending hello." in line or "UpdatePlayersJoined" in line:
        reader += line

with open('log.txt', 'w') as file:
    file.write(reader)
