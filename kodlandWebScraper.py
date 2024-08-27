from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from data.account import username, password
from utility.functions import getExercises
from progress.bar import Bar

import json, sys, time, os

start_time = time.time()

options = FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)
driver.maximize_window()

driver.get("https://backoffice.kodland.org/en/")

try:
    with open("data/data.json", "r") as f:
        data = json.loads(f.read())
except:
    data = {}

# ---------------------------- Login ----------------------------

while True:
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="id_username"]'))
        ).send_keys(username)
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="id_password"]'))
        )
        password_field.send_keys(password)
        password_field.submit()
        break
    except:
        print("Login element not found")
        driver.refresh()

# ------------------------ Verifica login ------------------------

while True:
    try:
        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://backoffice.kodland.org/en/courses/")
        )
        print("INFO - Login successful")
        driver.get("https://backoffice.kodland.org/en/groups/")
        break
    except:
        print("ERROR - Login failed")
        driver.refresh()

login_time = time.time() - start_time

# ------------------ Prendo la lista dei gruppi ------------------

if len(sys.argv) > 1:   # Se è stato passato un argomento
    try:
        groupsId = [sys.argv[1]]
    except:
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit("ERROR - Invalid group id\n")
else:
    try:
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='table_to_change']/table/tbody"))
        ).find_elements(By.TAG_NAME, "tr")

        groupsId = [] # Id dei gruppi

        for row in rows:
            groupsId.append(row.find_elements(By.TAG_NAME, "td")[0].text)
            if row.find_elements(By.TAG_NAME, "td")[0].text not in data:
                data[row.find_elements(By.TAG_NAME, "td")[0].text] = {}
        
        print("INFO - Groups found")
    except:
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit("ERROR - Groups table not found\n")

# ------------------ Ciclo per tutti i gruppi ------------------
    
group_time = []

for group in groupsId:
    # Vado alla pagina del gruppo 
    driver.get("https://backoffice.kodland.org/en/group_" + group + "/")

    # ------------------ Prendo informazioni gruppo ------------------

    try:
        data[group]["name"] = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Italy Python')]"))
        ).text.split(" ")[2].strip()

        data[group]["day"] = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Italy Python')]"))
        ).text.split("(")[1].split("-")[0].strip()

        data[group]["time"] = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//th[text()='Start']/following-sibling::td[1]"))
        ).text.split(" ")[1]

        data[group]["lessonNumber"] = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//th[text()='Lessons completed']/following-sibling::td[1]"))
        ).text.split("/")[0]

        if "students" not in data[group]:
            data[group]["students"] = []

        print(f"INFO - Group {group} data found")
    except:
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit(f"ERROR - Group {group} data not found\n")

    # ------------------ Click sulla tab "Controlla" ------------------
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Check']"))
        ).click()
    except:
        os.system("cls" if os.name == "nt" else "clear")
        sys.exit("ERROR - Controlla tab not found\n")

    # -----------------------------------------------------------------

    try:
        # ------------------ Prendo informazioni studenti ------------------

        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="table_body"]'))
        ).find_elements(By.TAG_NAME, "tr")

        studentLinks = []
        
        for i in range(len(rows)):
            student = {}
            th = rows[i].find_elements(By.TAG_NAME, "th")[0].find_elements(By.TAG_NAME, "a")[0]
            student["id"] = th.get_attribute("href").split("_")[1].split("/")[0]
            student["name"] = th.text
            exist = False
            for x in data[group]["students"]:
                if x["id"] == student["id"]:
                    exist = True
                    break
            if exist:
                continue
            studentLinks.append((i, th.get_attribute("href")))
            data[group]["students"].insert(i, student)

        print(f"INFO - Group {group} students data found")

        # ---------------- Inizializzo la lista di esercizi ----------------
        
        for i in range(len(data[group]["students"])):
            data[group]["students"][i]["lessons"] = []

        # ------------------- Ciclo per tutte le lezioni -------------------
            
        with Bar(f'INFO - Group {group} exercises data found', max = int(data[group]["lessonNumber"])) as bar:
        
            for i in range(int(data[group]["lessonNumber"])):
            
            # ------------------- Click per cambiare lezione -------------------
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element((By.XPATH, '//*[@id="dark-back"]'))
                    )
                    select = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/div[5]/div/div/div[1]/div/div/input")) # TODO: Non so se c'è di meglio
                    )
                    liId = select.get_attribute("data-target")
                    select.click()
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//li[@id='" + liId + str(i) + "']"))
                    ).click()
                except:
                    os.system("cls" if os.name == "nt" else "clear")
                    sys.exit("ERROR - Lesson click not found\n")

            # ---------------------------- Esercizi ----------------------------
                
                try:
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element((By.XPATH, '//*[@id="dark-back"]'))
                    )
                    tbody = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="table_body"]'))
                    ).get_attribute("innerHTML").split("<script>")[0]

                    data = getExercises(data, group, tbody)

                except:
                    os.system("cls" if os.name == "nt" else "clear")
                    sys.exit("ERROR - Exercises table problems\n")

                bar.next()

        # ----------------------- Numeri di telefono -----------------------

        if len(studentLinks) > 0:

            with Bar(f"INFO - Group {group} phone numbers found",max = len(studentLinks)) as bar:

                for i in range(len(studentLinks)):
                    driver.get(studentLinks[i][1])
                    a = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//th[text()=\"Parent's phone number\"]/following-sibling::td[1]/a"))
                    ).text.strip()
                    data[group]["students"][studentLinks[i][0]]["parentPhone"] = a if "+" in a else "+" + a

                    bar.next()

        # ------------------------------------------------------------------

    except Exception as e:
        #os.system("cls" if os.name == "nt" else "clear")
        sys.exit("ERROR - Students table problems\n" + str(e))

    group_time.append(time.time() - start_time)


# ----------------------- Scrivo i dati su file -----------------------
        
with open("data/data.json", "w") as f:
    f.write(json.dumps(data, indent=2))

os.system("cls" if os.name == "nt" else "clear")
print("SUCCESS - Aggiornamento dati completato\n")

# --------------------------------------------------------------------- 

driver.quit()
# print("--- Total time ---")
# print("--- %s seconds ---\n" % (time.time() - start_time))
# print("--- Login time ---")
# print("--- %s seconds ---\n" % login_time)
# for i in group_time:
#     print("--- Group time ---")
#     print("--- %s seconds ---\n" % i)