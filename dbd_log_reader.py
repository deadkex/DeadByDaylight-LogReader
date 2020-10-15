import os
import keyboard
from pathlib import Path
import json
path = os.path.expandvars(r'%LOCALAPPDATA%')

print("[Script by deadkex]")
# data ------------------------------------------------------------------------------------------------------------------
survivors = ["GS", "M", "ML", "D", "DF", "DK", "N", "NK", "BO", "MT", "C", "CM", "J", "JP", "SwedenSurvivor", "S22", "QM", "FM", "KS", "LS", "HS"]
killers = {
    "GK": "Clown",
    "CA": "Cannibal",
    "QK": "?",
    "DO": "Doctor",
    "DOW04": "Doctor",
    "SD": "Freddy",
    "OK": "Ghostface",
    "WI": "Hag",
    "TC": "Hillbilly",
    "KK": "Legion",
    "MM": "Myers",
    "TN": "Nurse",
    "FK": "Pig",
    "MK": "Plague",
    "HK": "Spirit",
    "SwedenKiller": "Oni",
    "TW": "Wraith",
    "TR": "Trapper",
    "WR": "Wraith",
    "HB": "Hillbilly",
    "NR": "Nurse",
    "HA": "Hag",
    "UK": "Deathslinger",
    "UkraineKiller": "Deathslinger",
    "BE": "Huntress",
    "Wraith": "Wraith",
    "TCW06": "Hillbilly",
    "Hillbilly": "Hillbilly",
    "K20": "Pyramid Head",
    "Nurse": "Nurse"
}
hotkeys = {
    "cfg": "ctrl+j",
    "logReader": "ctrl+k",
    "getKiller": "ctrl+h"
}
removeLog = False
cfg = {
    "survivors": survivors,
    "killers": killers,
    "hotkeys": hotkeys,
    "removeLog": removeLog
}


# cfg ---------------------------------------------------------------------------------------------------------------------
if Path("dbd_cfg.txt").is_file():
    with open('dbd_cfg.txt', 'r') as myfile:
        cfg = json.load(myfile)
    killers = cfg["killers"]
    survivors = cfg["survivors"]
    hotkeys = cfg["hotkeys"]
    removeLog = cfg["removeLog"]
    if removeLog is True:
        try:
            os.remove(path + '\\DeadByDaylight\\Saved\\Logs\\DeadByDaylight.log')
            print("-> DBD Logfile removed.")
            cfg["removeLog"] = False
            with open('dbd_cfg.txt', 'w') as my_file:
                json.dump(cfg, my_file, indent=4)
        except:
            print("-> Something is wrong here.")


def makeCfgFile():
    print("-> You can add killers/survivors and change or remove hotkeys in the dbd_cfg.txt file which will then be loaded when starting dbd_")
    if Path("dbd_cfg.txt").is_file():
        print("-> This will overwrite your configs. If that's what you want delete the dbd_cfg.txt file first and then try again.")
    else:
        with open('dbd_cfg.txt', 'w') as my_file:
            json.dump(cfg, my_file, indent=4)


# LogReader ----------------------------------------------------------------------------------------------------------------
def logReader():
    with open(path + '\\DeadByDaylight\\Saved\\Logs\\DeadByDaylight.log', 'r', encoding='utf-8') as file:
        try:
            x = file.readlines()
        except:
            print("-> Cannot read file. Try " + ("None" if hotkeys.get("cfg") is None else hotkeys.get("cfg")) + " + set removeLog to true + restart dbd_")
    reader = ""
    for line in x:
        if "LogCustomization: -->" in line or "Sending hello." in line or "UpdatePlayersJoined" in line:
            reader += line
    with open('dbd_log.txt', 'w') as file:
        file.write(reader)
    print("-> Log converted and saved as dbd_log.txt in the folder this was run from.")


# Main ---------------------------------------------------------------------------------------------------------------------
def getKiller():
    with open(path + '\\DeadByDaylight\\Saved\\Logs\\DeadByDaylight.log', 'r', encoding='utf-8') as file:
        try:
            x = file.readlines()
            x.reverse()
        except:
            print("-> Cannot read file. Try " + ("None" if hotkeys.get("cfg") is None else hotkeys.get("cfg")) + " + set removeLog to true + restart dbd_")
            return

    killername = ""
    killername2 = []  # Check for unknown survivors or killers
    for line in x:
        if killername != "" or "Sending hello." in line:  # Dont search the whole log; server says hello at the start of a new lobby
            break
        if "LogCustomization: -->" in line:  # f.e. [2020.07.16-14.04.08:949][861]LogCustomization: --> OK_Mask01
            for killer in killers:
                if ("--> " + killer + "_") in line:
                    killername = 'Killer: ' + killers[killer]  # + " | " + killer
                    timestamp = line.split("-", 1)[1].split(":", 1)[0].replace(".", ":")
                    if "LP01" in line:  # check for legacy
                        killername += " Legacy"
            try:
                t = line.split("--> ", 1)[1].split("_", 1)[0]  # get the unknown survs/killers
                if t not in survivors and t not in killers and t not in killername2:
                    killername2.append(t)
            except:
                pass
    if killername != "":
        print(timestamp + " | " + killername)
    else:
        print("Unknown killer.")
    if len(killername2) != 0:
        print(killername2)
        print("This could be an unknown survivor or killer, might want to check the log (" + hotkeys.get("logReader") + ") and add it to the config (" + hotkeys.get("cfg") + ").")


# hotkeys ------------------------------------------------------------------------------------------------------------------
print("GetKiller: " + ("None" if hotkeys.get("getKiller") is None else hotkeys.get("getKiller")) + " | MakeCfgFile: " + ("None" if hotkeys.get("cfg") is None else hotkeys.get("cfg")) + " | LogReader: " + ("None" if hotkeys.get("logReader") is None else hotkeys.get("logReader")))
print("-----------------------------------------------------------------")
if Path("dbd_cfg.txt").is_file():
    print("-> Config loaded from file.")
if hotkeys.get("getKiller") is not None:
    keyboard.add_hotkey(hotkeys["getKiller"], getKiller)
if hotkeys.get("cfg") is not None:
    keyboard.add_hotkey(hotkeys["cfg"], makeCfgFile)
if hotkeys.get("logReader") is not None:
    keyboard.add_hotkey(hotkeys["logReader"], logReader)
while True:
    pass
