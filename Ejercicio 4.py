# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 17:35:05 2024

@author: Karen
"""

import requests
import pandas as pd 
import json

#Endpoint del API 
url = "https://dogapi.dog/api/v2/breeds"

#solicitud GET
respuesta = requests.get(url) 

#verificar solicitud exitosa 
if respuesta.status_code == 200:
    print('Solicitud exitosa')
    print('Datos:', respuesta.json())
else:
    print("Error en la solicitud del recurso. Detalles:\n",
          respuesta.text)
    
# respuesta_json = respuesta_json()

print(respuesta.json())




