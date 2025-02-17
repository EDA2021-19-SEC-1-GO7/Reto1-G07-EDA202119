﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

from typing import cast
import config as cf
import sys
import controller as ctrl
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

default_limit = 1000
sys.setrecursionlimit(default_limit*10)

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Mostrar n videos con más likes que son tendencia en un país y de una categoría específica.")
    print("3- Video que ha sido trending por más días en un pais especifico con una percepción altamente positiva.")
    print("4- Video que ha sido trending por más días de categoria especifica con una percepción sumamente positiva.")
    print("5- Mostrar n videos con más comentarios, en un pais y con tag especifico.")
Data = None

def initialize()->dict:
    return ctrl.initialize()

def Load_Data(storage:dict)->None:
    ctrl.Load_Data(storage)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        Datos=initialize()      
        print("Cargando información de los archivos ....")
        Load_Data(Datos)
        print("Numero de videos cargados: "+str(lt.size(Datos["videos"])))
        first=lt.firstElement(Datos["videos"])
        print("Datos del primer video cargado:\n"+
            "Titulo: "+str(first["title"])+"\n"+
            "Canal: "+str(first["channel_title"])+"\n"+
            "Fecha de trending: "+str(first["trending_date"])+"\n"+
            "Pais: "+str(first["country"])+"\n"+
            "Vistas: "+str(first["views"])+"\n"+
            "Likes: "+str(first["likes"])+"\n"+
            "Dislikes: "+str(first["dislikes"])
        )
        print("Categorias: \n"+"id "+" nombre")
        for i in range(lt.size(Datos["categorias"])):
            cats=Datos["categorias"]
            elemento=lt.getElement(cats,i+1)
            id=elemento["id"]
            name=elemento["name"]
            print(id+" "+name)
        
    elif int(inputs[0]) == 2:
        pais=input("Pais: ")
        categoria=input("Categoria: ")
        n = input("Número de videos a listar: ")
        while int(n)>lt.size(Datos["videos"]):
            print("El número de videos a listar excede la cantidad de videos cargados en la memoria")
            n = input("Número de videos a listar: ")
        tiempo,lista=ctrl.filtrar_count_cat(Datos["videos"], Datos["categorias"], " "+categoria, pais) #El " " es porque cuando se leen las categorias, vienen con un espacio al inicio.
        i=1
        if lt.size(lista)==0:
            print("No hay videos que hayan sido tendencia en {} de la categoria {}".format(pais, categoria))
        while i<=lt.size(lista) and i<=int(n):
            vid=lt.getElement(lista,i)
            print("Titulo: "+vid["title"],"trending date: "+vid["trending_date"],"Canal: "+vid["channel_title"],"Fecha de publicacion: "+vid["publish_time"],"Vistas: "+vid["views"],"Likes: "+vid["likes"],"Dislikes: "+vid["dislikes"])
            i+=1
    elif int(inputs[0]) == 3:
        pais=input("Pais sobre el cual consultar: ")
        try:
            resultados=ctrl.max_vids_count(Datos["videos"], pais)
            print("\nTitulo: "+resultados[0],"\nCanal: "+resultados[2],"\npais: "+resultados[4],"\nRatio_likes/dislikes: "+str(resultados[1]),"\nNumero de dias: "+str(resultados[3]))
        except:
            print("No existe ningún video que haya sido tendencia en {} con una percepción altamente positiva".format(pais))
     
    elif int(inputs[0]) == 4:
        categoria= input("Categoria sobre la cual consultar: ")
        try:
            resultados=ctrl.max_vids_cat(Datos["videos"], Datos["categorias"], " "+categoria)
            print("\nTitulo: "+resultados[0], "\nCanal: "+resultados[2],"\nId de la Categroria: "+resultados[5],"\nRatio_likes/dislikes: "+str(resultados[1]),"\nNumero de dias: "+str(resultados[3]))
        except:
            print("No existe ningún video que haya sido tendencia de la categoria {} con una percepción sumamente positiva".format(categoria))

    elif int(inputs[0]) == 5:
        pais=input("Pais sobre el cual consultar: ")
        tag=input("Tag que desea consultar: ")
        n = input("Número de videos a listar: ")
        while int(n)>lt.size(Datos["videos"]):
            print("El número de videos a listar excede la cantidad de videos cargados en la memoria")
            n = input("Número de videos a listar: ")
        tiempo,lista=ctrl.filtrar_count_tag(Datos["videos"], pais, tag)        
        if lt.size(lista)==0:
            print("No hay videos que hayan sido tendencia con el tag {} y en {}".format(tag, pais))
        i=1
        while i<=lt.size(lista) and i<=int(n):
            vid=lt.getElement(lista, i)
            print("\nTitulo: "+vid["title"],"Canal: "+vid["channel_title"],"Fecha de publicacion: "+vid["publish_time"],"Vistas: "+vid["views"],"Likes: "+vid["likes"],"Dislikes: "+vid["dislikes"], "Cantidad de comentarios: "+vid["comment_count"], "Tags: "+vid["tags"])
            i+=1
            
    else:
        sys.exit(0)
sys.exit(0)