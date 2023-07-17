from django.shortcuts import render, redirect
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
# Create your views here.
def index(request):
    return render(request, "index.html")

def validate(request):
    id = request.POST.get('id')
    pswd = request.POST.get('pswd')
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    
    driver.get('https://rgmexams.co.in/Login.php')
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[1]/input").send_keys(id)
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[2]/input").send_keys(pswd)
    driver.find_element(By.XPATH, "/html/body/div/div/div[2]/form/div[3]/div[2]/button").click()
    time.sleep(1)
    driver.switch_to.new_window('tab')
    driver.get('https://rgmexams.co.in/IndividualCMM.php')
    driver.find_element(By.XPATH, "/html/body/div/div[1]/section[2]/div/div[2]/form/div/div[3]/button").click()
    rows = driver.find_elements(By.XPATH, "/html/body/div/div[1]/section[2]/div/div[2]/div/table[3]/tbody/tr")
    #print(len(rows), rows)
    grades = []
    temp = []
    cr = 0
    tot_cr = 0
    tot_grcr = 0
    count = 3
    for i in range(4,len(rows)+1):
        count +=1
        try:
            g = driver.find_element(By.XPATH, f"/html/body/div/div[1]/section[2]/div/div[2]/div/table[3]/tbody/tr[{count}]/td[5]").text
            c = driver.find_element(By.XPATH, f"/html/body/div/div[1]/section[2]/div/div[2]/div/table[3]/tbody/tr[{count}]/td[6]").text
            grcr = int(g) * float(c)
            temp.append(grcr)
            cr += float(c)
            tot_cr += float(c)
            tot_grcr += grcr
            print(g, c, cr)
        except Exception as e:
            #print(e)
            try:
                grades.append("{:.2f}".format(float(sum(temp)/cr)))
                #print(temp, sum(temp), cr)
            except:
                break
            #print(grades)
            cr = 0
            temp = []
            count += 4
    temp = []
    cr = 0
    count = 3
    for i in range(4,len(rows)+1):
        count +=1
        try:
            g = driver.find_element(By.XPATH, f"/html/body/div/div[1]/section[2]/div/div[2]/div/table[3]/tbody/tr[{count}]/td[11]").text
            c = driver.find_element(By.XPATH, f"/html/body/div/div[1]/section[2]/div/div[2]/div/table[3]/tbody/tr[{count}]/td[12]").text
            grcr = int(g) * float(c)
            temp.append(grcr)
            cr += float(c)
            tot_cr += float(c)
            tot_grcr += grcr
            print(g, c, cr)
        except:
            #print(g, c, cr)
            try:
                grades.append("{:.2f}".format(float(sum(temp)/cr)))
            except:
                break
            #print(grades)
            cr = 0
            temp = []
            count += 4
    print(tot_grcr, tot_cr, grades)
    final = "{:.2f}".format(tot_grcr/tot_cr)
    return render(request, "cgpa.html", {"cgpa" : final})