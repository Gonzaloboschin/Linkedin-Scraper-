###################### BUSCAMOS PERFILES ######################
#%%
from ntpath import join
from sre_constants import CATEGORY_NOT_DIGIT
import click
from joblib import PrintTime
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os



driver = webdriver.Chrome(r'C:\\Users\\gboschin\\Desktop\\API linkedin\\chromedriver.exe')
time.sleep(3) 


# Credenciales perfil fake
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



# localizamos las barras de busquedas y agregamos el puesto deseado
search = driver.find_element_by_xpath("//input[@aria-label='Buscar']")
keywords = 'Data Engineer'
search.send_keys(keywords)
search.send_keys(Keys.ENTER)
time.sleep(20)



personas = driver.find_elements_by_xpath("//button[@aria-label='Personas']")
personas = personas[0]
personas.click()
time.sleep(20)


candidatos = driver.find_elements_by_class_name("reusable-search__result-container")
time.sleep(20)
direcciones = list()

for i in range(len(candidatos)):
    direcciones.append(candidatos[i].find_elements_by_class_name("app-aware-link")[1].get_attribute('href'))

for x in direcciones:
    print(x)



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




df_profiles = pd.DataFrame(list(zip(name_list,cargo_list,locality_list,job_list,about_list,direcciones)),
                                 columns= ['Nombre','Cargo','Localidad','Trabajo','About','links'])

if os.path.exists('profiles.xlsx'):
    os.remove('profiles.xlsx')








direccion = direcciones[0]
driver.get(direccion)
driver.maximize_window()
time.sleep(3)

secciones = driver.find_elements_by_xpath("//section[contains(@class,'artdeco-card ember-view break-words pb3')]")

datos_perfil=[]

html_perfil = driver.find_element_by_xpath('//*[@id="profile-content"]/div/div[2]')


"""
sacamos la informacion de un perfil, pero hay que hacerlo dinamico, debido a que 
en este perfil la cantidad de bloques donde tiene experiencia, educacion, aptitudes, puede variar
por lo que las listas pueden no funcionar de esa forma
la forma que tengo que probar es usando la jerarquizacion de tags de HTML, reconocerlas, buscar
alguna diferencia y armar la lista asi

"""

#%%
experiencia_list_unique = []
educacion_list_unique = []
aptitudes_list_unique = []
idioma_list_unique = []
intereses_list_unique = []

experiencia_list = []
educacion_list = []
aptitudes_list = []
idioma_list = []
intereses_list = []


for item in secciones:
    item_str = str(item.text).split("\n")  

    if item_str[0] == "Experiencia":
        for item1 in range(len(item_str)):
            if item_str[item1] not in experiencia_list_unique:
                experiencia_list_unique.append(item_str[item1])
                strExperiencia = " ".join(experiencia_list_unique)
        experiencia_list.append(strExperiencia)
                
    
    if item_str[0] == "Educación":
        for item2 in range(len(item_str)):
            if item_str[item2] not in educacion_list_unique:
                educacion_list_unique.append(item_str[item2])
                strEducacion = " ".join(educacion_list_unique)
            educacion_list.append(strEducacion)


    if item_str[0] == "Conocimientos y aptitudes":
        for item3 in range(len(item_str)):
            if item_str[item3] not in aptitudes_list_unique:
                aptitudes_list_unique.append(item_str[item3])
                strAptitudes = " ".join(aptitudes_list_unique)
            aptitudes_list.append(strEducacion)

                
    if item_str[0] == "Idiomas":
        for item4 in range(len(item_str)):
            if item_str[item4] not in idioma_list_unique:
                idioma_list_unique.append(item_str[item4])
                strIdioma = " ".join(idioma_list_unique)
            idioma_list.append(strEducacion)


    if item_str[0] == "Intereses":
        for item5 in range(len(item_str)):
            if item_str[item5] not in intereses_list_unique:
                intereses_list_unique.append(item_str[item5])
                strIntereses = " ".join(intereses_list_unique)
            intereses_list.append(strIntereses)



#%%
if os.path.exists('info_profiles.xlsx'):
    os.remove('info_profiles.xlsx')

df_perfil = pd.DataFrame(list(zip(name_list,experiencia_list,educacion_list,aptitudes_list,idioma_list)),
                                 columns= ['Nombre','Experiencia','Educacion','Conocimiento y Aptitudes','Idiomas'])



profiles = 'info_profile.xlsx'
df_perfil.to_excel("info_profile.xlsx")

#%%

"""
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



