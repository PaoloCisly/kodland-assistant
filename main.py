from utility.functions import getUncheckedExercises, getStatusExercises
from utility.messagesWA import messagesWA

import json, webbrowser, time, os

# ----------- Controllo ultimo aggiornamento dati -----------

updated = False

try:
    with open("data/lastUpdate.txt", "r") as f:
        lastUpdate = f.read()
        if int(time.time()) - int(lastUpdate) > 3600*4:
            os.system("cls" if os.name == "nt" else "clear")
            print("Aggiornamento dei dati...\n")
            os.system("python kodlandWebScraper.py")
            updated = True
    
    with open("data/lastUpdate.txt", "w") as f:
        f.write(str(int(time.time())))
except:
    with open("data/lastUpdate.txt", "w") as f:
        f.write(str(int(time.time())))

# ------------------ Leggo i dati dal file ------------------

if not updated:
    os.system("cls" if os.name == "nt" else "clear")

data = {}
try:
    with open("data/data.json", "r") as f:
        data = json.loads(f.read())
except:
    print("Creazione dei dati...\n")
    os.system("python kodlandWebScraper.py")
    with open("data/data.json", "r") as f:
        data = json.loads(f.read())
    time.sleep(3)

# ------------------ Stampo la lista dei gruppi ------------------

while True:

    lst = [f'{data[group]["day"]} {data[group]["name"]}' for group in data]

    print("------- Gruppi -------")
    for i in range(len(lst)):
        print(f" {i+1} - {lst[i]}")
    print("\n 9 - Aggiorna i dati")
    print(" 0 - Esci")
    print("----------------------")

    while True:
        terminal = input("\nSeleziona un gruppo: ")

        if terminal == "0":
            exit()

        elif terminal.isdigit() and 0 < int(terminal) <= len(lst):
            groupName = lst[int(terminal)-1]
            group = list(data.keys())[int(terminal)-1]
            break

        elif terminal == "9":
            os.system("cls" if os.name == "nt" else "clear")
            print("Aggiornamento dei dati...\n")
            os.system("python kodlandWebScraper.py")

            with open("data/data.json", "r") as f:
                data = json.loads(f.read())
            
            with open("data/lastUpdate.txt", "w") as f:
                f.write(str(int(time.time())))

            break

        else:
            print("Errore: selezione non valida")

    if terminal == "9": # Aggiornamento dei dati, torna su
        continue

    while True:
        option = -1
        if option != 1:
            os.system("cls" if os.name == "nt" else "clear")
        print(f"\n---------- Gruppo {groupName} ----------")
        print(" 1 - Esercizi da correggere")
        print(" 2 - Status esercizi")
        print(" 3 - Modifica numeri di telefono")
        print("\n 9 - Indietro")
        print(" 0 - Esci")
        print("------------------------------------")

        while True:
            terminal = input("\nSeleziona un'opzione: ")

            if terminal == "0":
                exit()
            elif terminal.isdigit() and (0 < int(terminal) <= 3 or int(terminal) == 9):
                option = int(terminal)
                break
            else:
                print("Errore: selezione non valida")

        if option == 9:
            os.system("cls" if os.name == "nt" else "clear")
            break
        elif option == 1:
            links = getUncheckedExercises(data[group])
            if links:
                numlinks = 0
                for link in links:
                    if link:
                        numlinks += 1
                print(f"\nHai {numlinks} compiti da correggere")
                print("Apertura di Firefox...")
                webbrowser.register('firefox', None, webbrowser.BackgroundBrowser("C:/Program Files/Mozilla Firefox/firefox.exe"))

                controller = webbrowser.get('firefox')
                controller.open(f"https://backoffice.kodland.org/it/group_{group}/#test2")
                time.sleep(10)

                noneCount = 0
                for i in range(len(links)):
                    if links[i]:
                        controller.open(links[i], new=1)
                        time.sleep(0.1)
                    else:
                        noneCount += 1
                        if numlinks-i-1+noneCount > 0:
                            input(f"Mancano {numlinks-i-1+noneCount} esercizi. Premi invio per continuare...")
                        else:
                            break
                
                print("\nTutti gli esercizi sono stati aperti")
                input("\nPremi invio per aggiornare i dati...")

                os.system("cls" if os.name == "nt" else "clear")
                print("Aggiornamento dei dati...\n")

                os.system(f"python kodlandWebScraper.py {group}")

                with open("data/data.json", "r") as f:
                    data = json.loads(f.read())

                with open("data/lastUpdate.txt", "w") as f:
                    f.write(str(int(time.time())))
                    
            else:
                print("\nNessun esercizio da correggere")
                time.sleep(2)

        elif option == 2:
            statusExercises = getStatusExercises(data[group])
            messagesWA(statusExercises)
            continue

        elif option == 3:
            for student in data[group]["students"]:
                if "phone" not in student:
                    print(f"\n{student['name']}")
                    phone = input("Inserisci il numero di telefono: ").strip()
                    if phone != "":
                        student["phone"] = phone
                        if phone == student["parentPhone"]:
                            student["parentPhone"] = ""
                else:
                    if student["parentPhone"] == "":
                        print(f"\nNO PARENT PHONE - {student['name']}")

            with open("data/data.json", "w") as f:
                f.write(json.dumps(data, indent=4))

            print("\nSUCCESS - Dati salvati correttamente")
            time.sleep(2)

        else:
            print("Errore: selezione non valida")