###################### BUSCAMOS TRABAJOS ######################
#%%
import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np






driver = webdriver.Chrome(r"C:\\Users\\gboschin\\Desktop\\API linkedin\\chromedriver.exe")



# credenciales de perfil fake
email = "elincognito1996@gmail.com"
password = "holamundo123"



driver.get('https://www.linkedin.com/login') 
driver.maximize_window()
time.sleep(3) 



driver.find_element(By.ID, 'username').send_keys(email)            
driver.find_element(By.ID, 'password').send_keys(password)
driver.find_element(By.ID, 'password').send_keys(Keys.RETURN)



driver.get("https://www.linkedin.com/jobs/")
time.sleep(1)


# localizamos las barras de busquedas y agregamos el puesto deseado
search_bars = driver.find_elements(By.CLASS_NAME,'jobs-search-box__text-input')
keywords = 'Data Engineer'
search_keywords = search_bars[0]    
search_keywords.send_keys(keywords)
time.sleep(1)

location = 'Argentina'    
search_location = search_bars[3]
search_location.send_keys(location)
time.sleep(1)
search_location.send_keys(Keys.ENTER)






# sacamos una lista de todos los elementos de los anuncios en la barra lateral
list_item = driver.find_elements(By.CLASS_NAME, "occludable-update")






position_list = []
company_list = []
location_list = []
applications_list = []
posted_list = []
details_list = []




# desplaza una sola pagina
for job in list_item:
    # ejecuta JavaScript para desplazar el div a la vista
    driver.execute_script("arguments[0].scrollIntoView();", job)
    job.click()
    time.sleep(3)
    
    # obtenemos informacion
    position = job.text.split('\n')[0]
    company = job.text.split('\n')[1]
    location = job.text.split('\n')[2]
    posted_date = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__posted-date").text    
    details = driver.find_element(By.ID, "job-details").text
    #applications = driver.find_element(By.CLASS_NAME, "jobs-unified-top-card__applicant-count").text    
    

    #Appendeo los detalles a una lista
    position_list.append(position)
    company_list.append(company)
    location_list.append(location)
    #applications_list.append(applications)
    posted_list.append(posted_date)
    details_list.append(details)



data = pd.DataFrame(list(zip(position_list,company_list,location_list,posted_list,details_list)),
                columns= ['Posicion','Compañia','Location','Posteado','Detalles'])



print(data)


Jobs = 'jobs.csv'
data.to_csv("jobs.csv")

