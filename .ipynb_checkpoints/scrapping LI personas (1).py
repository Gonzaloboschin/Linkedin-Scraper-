###################### BUSCAMOS PERFILES ######################
import datetime
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os

print("Linkedin Scrapper - Inicio")
inicio = datetime.datetime.now() 
driver = webdriver.Chrome(r'C:\\Users\\gboschin\\Desktop\\API linkedin\\chromedriver.exe')
time.sleep(3) 

email = "elincognito1996@gmail.com"
password = "holamundo123"

driver.get('https://www.linkedin.com/login') 
driver.maximize_window()
time.sleep(3) 

driver.find_element(By.ID, 'username').send_keys(email) 
driver.find_element(By.ID, 'password').send_keys(password)
driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)
time.sleep(5)

driver.get("https://www.linkedin.com/")
time.sleep(5)

search = driver.find_element_by_xpath("//input[@aria-label='Buscar']")
keywords = 'Data Engineer'
search.send_keys(keywords)
search.send_keys(Keys.ENTER)
time.sleep(20)

personas = driver.find_elements_by_xpath("//button[@aria-label='Personas']")
time.sleep(3)
personas = personas[0]
personas.click()
time.sleep(20)


candidatos = driver.find_elements_by_class_name("reusable-search__result-container")
time.sleep(20)
direcciones = list()

for i in range(len(candidatos)):
    direcciones.append(candidatos[i].find_elements_by_class_name("app-aware-link")[1].get_attribute('href'))


# tomamos todos los valores del html    

list_item = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container ")
search_bars = driver.find_elements_by_class_name('search-reusables__filters-bar-grouping')  # fijarse su sta al pedo
time.sleep(20)

name_list = []
cargo_list = []
locality_list = []
about_list = []
job_list = []

n=1
for people in list_item:

    people_str = str(people.text).split("\n")
    name = people_str[0]
    cargo = people_str[4]
    locality = people_str[5]
    job = people_str[6]
    about = " " 
    
    name_list.append(name)
    cargo_list.append(cargo)
    locality_list.append(locality)
    job_list.append(job)
    about_list.append(about)

if os.path.exists('profiles.xlsx'):
    print('si existe')
    os.remove('profiles.xlsx')

df_profiles = pd.DataFrame(list(zip(name_list,cargo_list,locality_list,job_list,about_list,direcciones)),
                                 columns= ['Nombre','Cargo','Localidad','Trabajo','About','links'])
df_profiles.to_excel('profiles.xlsx', sheet_name='Profiles', index=False)

experiencia_list_unique = []
educacion_list_unique = []
licencias_list_unique = []
aptitudes_list_unique = []
idioma_list_unique = []
intereses_list_unique = []

experiencia_list = []
educacion_list = []
licencias_list = []
aptitudes_list = []
idioma_list = []
intereses_list = []

for perfil in direcciones:
    driver.get(perfil)
    time.sleep(3)
    
    secciones = driver.find_elements_by_xpath("//section[contains(@class,'artdeco-card ember-view break-words pb3')]")

    for item in secciones:
        item_str = str(item.text).split("\n")  

        if item_str[0] == "Experiencia":
            for item1 in range(len(item_str)):
                if item_str[item1] not in experiencia_list_unique and item_str[item1] != "Experiencia":
                    experiencia_list_unique.append(item_str[item1])
            
            strExperiencia = " ".join(experiencia_list_unique)
            experiencia_list_unique = []
            experiencia_list.append(strExperiencia)
            strExperiencia = " "
            
        if item_str[0] == "Educación":
            for item2 in range(len(item_str)):
                if item_str[item2] not in educacion_list_unique and item_str[item2] != "Educación":
                    educacion_list_unique.append(item_str[item2])
            strEducacion = " ".join(educacion_list_unique)
            educacion_list_unique.clear()
            educacion_list.append(strEducacion)
            strEducacion = " "

        if item_str[0] == "Licencias y Certificaciones":
            for item2 in range(len(item_str)):
                if item_str[item2] not in licencias_list_unique:
                    licencias_list_unique.append(item_str[item2])
            strLicencias = " ".join(licencias_list_unique)
            licencias_list_unique.clear()
            licencias_list.append(strLicencias)
            strLicencias = " "

        if item_str[0] == "Conocimientos y aptitudes":
            for item3 in range(len(item_str)):
                if item_str[item3] not in aptitudes_list_unique and item_str[item3] != "Conocimientos y aptitudes":
                    aptitudes_list_unique.append(item_str[item3])
            strAptitudes = " ".join(aptitudes_list_unique)
            aptitudes_list_unique.clear()
            aptitudes_list.append(strAptitudes)
            strAptitudes = " "
                    
        if item_str[0] == "Idiomas":
            for item4 in range(len(item_str)):
                if item_str[item4] not in idioma_list_unique and item_str[item4] != "Idiomas":
                    idioma_list_unique.append(item_str[item4])
            strIdioma = " ".join(idioma_list_unique)
            idioma_list_unique.clear()
            idioma_list.append(strIdioma)
            strIdioma = " "

        if item_str[0] == "Intereses":
            for item5 in range(len(item_str)):
                if item_str[item5] not in intereses_list_unique and item_str[item5] != "Intereses":
                    intereses_list_unique.append(item_str[item5])
            strIntereses = " ".join(intereses_list_unique)
            idioma_list_unique.clear()
            intereses_list.append(strIntereses)
            strIntereses = " "

#html_perfil = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]')

"""
print(len(name_list))
print(len(cargo_list))
print(len(about_list))
print(len(locality_list))
print(len(experiencia_list))
print(len(educacion_list))
print(len(licencias_list))
print(len(aptitudes_list))
print(len(idioma_list)) # idioma no estan entrando los 10 
print('intereses: ', len(intereses_list))"""


if os.path.exists('info_perfiles.xlsx'):
    print('si existe')
    os.remove('info_perfiles.xlsx')

df_profiles = pd.DataFrame(list(zip(name_list,cargo_list,about_list,locality_list,experiencia_list,educacion_list,licencias_list,aptitudes_list)),
                                 columns= ['Nombre','Cargo','About','Localidad','Experiencia','Educacion', 'Licencias y Certificaciones', 'Aptitudes'])
df_profiles.to_excel('info_perfiles.xlsx')

"""
datos_perfil = []

for item in datos_perfil:
    perfil_str = item.sopk
    experiencia = perfil_str[0]


for s in secciones:
    prueba = s.find_element_by_tag_name('h2')
    palabra = prueba.get_attribute("innerText")


if palabra.splitlines()[1] == 'Experiencia':
    experiencia = s
    

trabajos = experiencia.find_elements_by_tag_name('ul')


for t in trabajos:
    print("---------------------")
text = t.get_attribute("innerText")
print("\n", text)

"""


fin = datetime.datetime.now()   
print("Tiempo de ejecucción: ", fin - inicio, " segundos")


