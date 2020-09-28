import csv
importaciones= []
exportaciones= []

with open("synergy_logistics_database.csv", "r") as archivo_csv:
    lector= csv.DictReader(archivo_csv)
    
    for linea in lector:
        if linea['direction']=='Exports':
            exportaciones.append(linea)
        elif linea['direction']=='Imports':
            importaciones.append(linea)
            
def valor_de_ruta(direccion,key): #Recibe direccion del viaje y criterio de clasificación en forma de llave
    rutas_existentes={} #Crea diccionario vacío
    for ruta in direccion:
        if key=='ruta':
            ruta_actual = ruta['origin'] +'-'+ ruta['destination'] #Crea un string con el nombre de la ruta
        else:
            ruta_actual= ruta[key] ##ruta[key]
          
        if ruta_actual not in rutas_existentes.keys():
            rutas_existentes.setdefault(ruta_actual,{}) #El nombre de la ruta se usa como llave de un subdiccionario
            rutas_existentes[ruta_actual].setdefault('viajes',0)
            rutas_existentes[ruta_actual].setdefault('valor',0)
        else: #Si la ruta ya existe como subdiccionario, se suman los valores del viaje 
            rutas_existentes[ruta_actual]['viajes']+=1
            rutas_existentes[ruta_actual]['valor']+=int(ruta['total_value'])    
    
    #Convertir diccionario a lista
    lista=[] #Crea una lista con los valores obtenidos [origen, destino, viajes, valor]
    for elemento, numero in rutas_existentes.items():
        lista.append([elemento, numero['viajes'], numero['valor']])
        
    return lista

def mostrar_valores(data, criterio, top):
    space=' '*(26-len(criterio))
    print(f'{criterio}{space}VIAJES                    VALOR')
    for ruta in data[:top]:
        space1=' '*(28-len(ruta[0]))
        space2=' '*(21-len(str(ruta[1])))
        valor='$'+'{:,}'.format(int(ruta[2]))
        print(f'{ruta[0]}{space1}{ruta[1]}{space2}{valor}')
    
def mostrar_valores2(data, total):
    print(f'PAÍS                        VALOR         PORCENTAJE     VIAJES')
    i=0
    porcentaje=0
    while porcentaje/total<=0.8:
        valor='$'+'{:,}'.format(int(data[i][2]))
        porcentaje_actual= str(round(int(data[i][2])/total*100,2))+' %'
        
        space1=' '*(23-len(data[i][0]))
        space2=' '*(14-len(porcentaje_actual))
        space3=' '*(10-len(str((data[i][1]))))
        
        print(f'{data[i][0]}{space1}{valor}{space2}{porcentaje_actual}{space3}{data[i][1]}')
        porcentaje+=data[i][2]
        i+=1
        
#CONSIGNA 1: Encontrar las 10 rutas más demandadas acorde a flujos de importación y exportación
        
valores_exportacion=valor_de_ruta(exportaciones,'ruta')
valores_exportacion.sort(reverse=True, key= lambda x:x[1]) #Ordena según demanda de viajes
print('|||||||||||| EXPORTACIONES CON MAYOR DEMANDA |||||||||||||||')
mostrar_valores(valores_exportacion, 'RUTA', 10)

valores_exportacion.sort(reverse=True, key= lambda x:x[2]) #Ordena según demanda de viajes
print('||||||||||||| EXPORTACIONES CON MAYOR VALOR ||||||||||||||||')
mostrar_valores(valores_exportacion, 'RUTA', 10)

valores_importacion=valor_de_ruta(importaciones,'ruta')
valores_importacion.sort(reverse=True, key= lambda x:x[1]) #Ordena según demanda de viajes
print('\n|||||||||||| IMPORTACIONES CON MAYOR DEMANDA |||||||||||||||')
mostrar_valores(valores_importacion, 'RUTA', 10)

valores_importacion.sort(reverse=True, key= lambda x:x[2]) #Ordena según demanda de viajes
print('|||||||||||||| IMPORTACIONES CON MAYOR VALOR |||||||||||||||||')
mostrar_valores(valores_importacion, 'RUTA', 10)

#CONSIGNA 2: Encontrar los 3 medios de transporte considerando valor de importaciones y exportaciones

valores_transporte=valor_de_ruta(importaciones,'transport_mode')
valores_transporte.sort(reverse=True, key= lambda x:x[2]) 
print('\n|||||||||||| IMPORTANCIA DE LOS MEDIOS DE TRANSPORTE |||||||||||||||')
mostrar_valores(valores_transporte, 'TRANSPORTE', 4)

#CONSIGNA 3: Encontrar paises que generan el 80% de las ganancias 

total_imp=0
for element in valores_importacion:
    total_imp+=element[2]   
    
valor_pais_imp=valor_de_ruta(importaciones, 'destination')
valor_pais_imp.sort(reverse=True, key= lambda x:x[2])
print('\n||||||||||||||| PAISES CON MAYOR VALOR DE IMPORTACIÓN |||||||||||||||||||')
mostrar_valores2(valor_pais_imp, total_imp)


total_exp=0
for element in valores_exportacion:
    total_exp+=element[2] 
valor_pais_exp=valor_de_ruta(exportaciones, 'origin')
valor_pais_exp.sort(reverse=True, key= lambda x:x[2])
print('\n||||||||||||||| PAISES CON MAYOR VALOR DE EXPORTACIÓN |||||||||||||||||||')
mostrar_valores2(valor_pais_exp, total_exp)