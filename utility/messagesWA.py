import time, os, webbrowser, pyautogui
import pyperclip as pc
from progress.bar import Bar

def messagesWA(statusExercises):
    # ------------------------ Creazione messaggi ------------------------

    print("\n--------------- Status Esercizi ---------------\n")

    messages = []

    for student in statusExercises:
        print(f"{student['name']}:")

        message = ""

        if student['points'][0] >= student['points'][1]:        # Se ha raggiunto il massimo punteggio
            print(">> Massimo punteggio raggiunto\n")

            with open('whatsappTemplate/goodWork.txt', 'r', encoding="UTF-8") as f:
                message = f.read()

        elif all(lesson[1] == 0 for lesson in student["lessons"]):      # Se ha inviato tutti gli esercizi
            print("  - Inviati tutti gli esercizi")
            print(f">> Punti totali: {student['points'][0]}/{student['points'][1]}\n")

            with open('whatsappTemplate/checkPoints.txt', 'r', encoding="UTF-8") as f:
                message = f.read()

            message = message.format(points=f"{student['points'][0]}/{student['points'][1]}")

        else:                                                   # Se non ha inviato tutti gli esercizi
            nModules = int(len(student["lessons"])/4)
            exercises = ""
            for i in range(nModules):
                modulePoints = 0
                for j in range(4):
                    modulePoints += student["lessons"][j + i*4][1]
                if modulePoints != 0:
                    print(f"  - Modulo {i+1}: {modulePoints} esercizi non inviati")
                    exercises += f"- Modulo {i+1} - Ti mancano {modulePoints} esercizi\n"
            for i in range(nModules*4, len(student["lessons"])):
                if student["lessons"][i][1] != 0:
                    print(f"  - {student['lessons'][i][0].split(' ')[0]}: {student['lessons'][i][1]} esercizi non inviati")
                    if student["lessons"][i][1] > 1:
                        exercises += f"- {student['lessons'][i][0].split(' ')[0]} - Ti mancano {student['lessons'][i][1]} esercizi\n"
                    else:
                        exercises += f"- {student['lessons'][i][0].split(' ')[0]} - Ti manca {student['lessons'][i][1]} esercizio\n"
            print(f">> Punti totali: {student['points'][0]}/{student['points'][1]}\n")

            with open('whatsappTemplate/checkExercises.txt', 'r', encoding="UTF-8") as f:
                message = f.read()

            message = message.format(exercises=exercises, points=f"{student['points'][0]}/{student['points'][1]}")
        
        messages.append(message)

    while True:
        terminal = input("\nVuoi inviare i messaggi su WhatsApp? (yes/n): ")
        if terminal.lower() == "yes":
            os.system("cls" if os.name == "nt" else "clear")
            print("\nNon usare il computer durante l'invio dei messaggi.")
            time.sleep(3)
            print("\nINFO - Invio messaggi su WhatsApp...")
            break
        elif "y" in terminal.lower():
            print("Inserire yes per confermare l'invio dei messaggi.")
        else:
            return


    # ------------------------ Invio messaggi ------------------------

    BASE_URL = "https://web.whatsapp.com/"
    # CHAT_URL = "https://web.whatsapp.com/send?phone={phone}&type=phone_number&app_absent=1"

    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))

    controller = webbrowser.get('chrome')

    print("INFO - Apertura chrome...")
    os.system('"C:\Program Files\Google\Chrome\Application\chrome.exe"')
    time.sleep(2)

    print("INFO - Apertura WhatsApp...")
    controller.open(BASE_URL)
    time.sleep(15)

    with Bar(f'INFO - Messaggi inviati',max = len(messages)) as bar:
        for i in range(len(messages)):
            # search for the chat
            pc.copy(statusExercises[i]["phone"])
            pyautogui.hotkey('ctrl', 'alt', '/')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)

            # send the message
            pc.copy(messages[i])
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            pyautogui.press('enter')
            time.sleep(1)

            bar.next()

    # close the browser
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(0.2)

    print("\nSUCCESS - Messaggi inviati correttamente.")
    input("\nPremi invio per continuare...")