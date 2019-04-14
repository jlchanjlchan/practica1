# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 04:30:40 2019

@author: Jin Lung i Eric Ariño
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd

#definició de variables

URL_BASE = "https://www.habitaclia.com/alquiler-barcelona-"
#modificació de l'user agent
headers = {'User-Agent': 'Mozilla/5.0'}
MAX_PAGES = 10
counter = 0
d=[]
preus=[]
preuslength=14

#control de les restriccions del ftixer robots.txt
response = requests.get('https://www.habitaclia.com/robots.txt')
robots = response.text
print("\nFitxer robots.txt de https://www.habitaclia.com")
print("Verificació de restriccions:\n")
print(robots)

print("\nRealitzant scraping")

#bucle per recorrer les  pagines d'habitaclia
for i in range(1, MAX_PAGES):

    if i < 1:
        url = URL_BASE
    else:
        url = "%s%d.htm" % (URL_BASE, i)
        print(url)
        req = requests.get(url,headers=headers)
    # Comprovem que la petició retorna Status Code = 200
        statusCode = req.status_code
        
        if statusCode == 200:
            
        # Pasem el contingut HTML de la web a un objecte BeautifulSoup()
            html = BeautifulSoup(req.text, "html.parser")
            
        # Obtenim tots els divs de les entrades
            panell = html.find(id="js-list")
            entradas = panell.find_all(class_="list-item-content")
            
        # Recorrem totes les entrades per l'extracció de dades rellevants
            for entrada in entradas:
               
                #Barri on s'han publicat els anuncis:
                barri = entrada.find(class_ = 'list-item-location').get_text()
                
                #tipus d'immoble dels anuncis                
                TipusImmoble = entrada.find(class_= 'list-item-title').get_text()
                             
                #Bucle pels preus dels anuncis
                tot_preus = panell.select(".list-item-content-second .font-2")
                preus = [pt.get_text() for pt in tot_preus]
                preuslenght= len(preus)
              
                #Metres quadrats dels anuncis:
                metres = entrada.find(class_= 'list-item-feature').get_text()
                
                #Numero de lavabos dels anuncis:
                lavabos = entrada.find(class_= 'list-item-feature').get_text()
                
                #Numero d'habitacoins dels anuncis:
                habitacions = entrada.find(class_= 'list-item-feature').get_text()
                
                #Breu descripcio dels anuncis                
                descripcio = entrada.find(class_= 'list-item-title').get_text()
                
            
            # S'afegeix els elements extrets a la llista per columnes

                d.append({
                       "Barri": barri,
                       "TipusImmoble": TipusImmoble,
                       "Preu": preus[counter],
                       "Metres": metres,
                       "Lavabo": lavabos ,
                       "Habitacions": habitacions,                      
                       "Descripció": descripcio,
                      })
                    
           #convertim la llista en una DataFrame de Panda
                taula=pd.DataFrame(d)
                
                #a través de expressions regulars s'extreu només el contingut necessari
                taula['Descripció']=taula.TipusImmoble.str.extract('Alquiler .+?\s\s(.+)')
                taula['Habitacions']=taula.Habitacions.str.extract('.+(\d+) habitaciones')
                taula['Barri']=taula.Barri.str.extract('Barcelona - (.+)')
                taula['TipusImmoble']=taula.TipusImmoble.str.extract('Alquiler (.+?)\s')
                taula['Metres']=taula.Metres.str.extract('(\d+)')
                taula['Lavabo']=taula.Lavabo.str.extract('.+(\d+) baño')
               
              
                #comptador per recorrer l'index de preus.
                counter += 1 
                
                if counter>preuslength:
                   counter=0
                
       else:
        # Si no existeix la página i retorna error 400
            break 

#es genera un fitxer del dataset 
taula.to_csv('habitaclia_pisos_barcelona_abril_2019.csv',encoding='utf-16')
