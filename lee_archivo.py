import os, sys, glob
from bs4 import BeautifulSoup
from operator import itemgetter
import requests, re
import time

info = ""
#Constantes
TAM_MAX = 50

def obtenerTitulos():
    global info
    global soup
    # Titulo principal
    title = soup.h1.text
    info += title + "\n"
    #Titulo secundario
    title2 = soup.h2.text
    info += title2 + "\n\n"
    
def obtenerIdDoujinshi():
    global doujinshi_id
    global info
    doujinshi_id = soup.h3.text
    info += doujinshi_id + "\n\n"
    
def obtenerIDGaleria():
    global doujinshi_id
    global gallery_id
    global gall
    global info
    
    galos = soup.find('img', class_='lazyload')
    gall_id = galos.noscript.img.get('src')
    cadena = format(gall_id)
    separador = "/"
    gallery_id = cadena.split(separador)
    
def llenadoDeLista():
    global atributos
    global list_sections
    atr = format(atributos)
    if "Parodies" in atr:
        list_sections[0] = True
    if "Characters" in atr:
        list_sections[1] = True
    if "Tags" in atr:
        list_sections[2] = True
    if "Artists" in atr:
        list_sections[3] = True
    if "Groups" in atr:
        list_sections[4] = True
    if "Languages" in atr:
        list_sections[5] = True
    if "Categories" in atr:
        list_sections[6] = True
    if "Pages" in atr:     
        list_sections[7] = True
        
def llenadoDeListasDeAtributos():
    global list_sections
    global atributos
    global list_parodies
    global list_characters
    global list_tags
    global list_artists
    global list_groups
    global list_languages
    global list_categories
    global list_pages
    global no_pag
    cont = 0

    #Parodies
    if list_sections[0] != False:
        subcat = atributos[cont].text.split("\n\n")
        if subcat[0].lstrip() == "Parodies":
            cadena = atributos[cont]
            parodies = cadena.find_all('span', class_='name')
            for parody in parodies:
                list_parodies.append(parody.text)
        cont += 1
    #Characters
    if list_sections[1] != False:
        subcat = atributos[cont].text.split("\n\n")
        if subcat[0].lstrip() == "Characters":
            cadena = atributos[cont]
            characters = cadena.find_all('span', class_='name')
            for character in characters:
                list_characters.append(character.text)
        cont += 1
    #Tags
    if list_sections[2] != False:
        subcat = atributos[cont].text.split("\n\n")
        if subcat[0].lstrip() == "Tags":
            cadena = atributos[cont]
            tags = cadena.find_all('span', class_='name')
            for tag in tags:
                list_tags.append(tag.text)
        cont += 1
    #Artists
    if list_sections[3] != False:
        subcat = atributos[cont].text.split("\n\n")
        if subcat[0].lstrip() == "Artists":
            cadena = atributos[cont]
            artists = cadena.find_all('span', class_='name')
            for artist in artists:
                list_artists.append(artist.text)
        cont += 1
    #Groups
    if list_sections[4] != False:
        subcat = atributos[cont].text.split("\n\n")
        if subcat[0].lstrip() == "Groups":
            cadena = atributos[cont]
            groups = cadena.find_all('span', class_='name')
            for group in groups:
                list_groups.append(group.text) 
        cont += 1
    #Languages
    if list_sections[5] != False:
        subcat = atributos[cont].text.split("\n\n")
        if subcat[0].lstrip() == "Languages": 
            cadena = atributos[cont]
            languages = cadena.find_all('span', class_='name') 
            for language in languages:  
                list_languages.append(language.text)   
        cont += 1
    #Categories
    if list_sections[6] != False:
        subcat = atributos[cont].text.split("\n\n")
        if subcat[0].lstrip() == "Categories": 
            cadena = atributos[cont]
            categories = cadena.find_all('span', class_='name') 
            for category in categories:  
                list_categories.append(category.text)   
        cont += 1
    #Pages
    if list_sections[7] != False:
        subcat = atributos[cont].text.split(":")
        if subcat[0].lstrip() == "Pages": 
            cadena = atributos[cont]
            pages = cadena.find_all('span', class_='name') 
            for page in pages:  
                list_pages.append(page.text)   
        cont += 1
    cad_aux = format(list_pages[0])
    no_pag = int(cad_aux)
    
def impresionDeListasAtributos():
    global list_parodies
    global list_characters
    global tam_max
    global info
    global url

    #Parodies
    if len(list_parodies) != 0:
        info += "Parodies: "
        count = 0
        while count < len(list_parodies):
            if count == len(list_parodies)-1:
                info += list_parodies[count]
            else:          
                info += list_parodies[count] + ", "
            count += 1
        info += "\n"
    #Characters
    if len(list_characters) != 0:
        info += "Characters: "
        count = 0
        tam_cad = 12
        while count < len(list_characters):
            if count == len(list_characters)-1:
                info += list_characters[count]
            else:          
                if(tam_cad < TAM_MAX):
                    info += list_characters[count] + ", "
                    tam_cad += (len(list_characters[count]) + 2)
                else:
                    info += "\n\t"
                    tam_cad = 4
            count += 1
        info += "\n"
    #Tags
    if len(list_tags) != 0:
        info += "Tags: "
        count = 0
        tam_cad = 6
        while count < len(list_tags):
            if count == len(list_tags)-1:
                info += list_tags[count]
            else:
                if(tam_cad < TAM_MAX):
                    info += list_tags[count] + ", "
                    tam_cad += (len(list_tags[count]) + 2)
                else:
                    info += "\n\t"
                    tam_cad = 4                    
            count += 1
        info += "\n"
    #Artists
    if len(list_artists) != 0:
        info += "Artists: "
        count = 0
        tam_cad = 9
        while count < len(list_artists):
            if count == len(list_artists)-1:
                info += list_artists[count]
            else:
                if(tam_cad < TAM_MAX):
                    info += list_artists[count] + ", "
                    tam_cad += (len(list_artists[count]) + 2)
                else:
                    info += "\n\t"
                    tam_cad = 4  
            count += 1
        info += "\n"
    #Groups
    if len(list_groups) != 0:
        info += "Groups: "
        count = 0
        while count < len(list_groups):
            if count == len(list_groups)-1:
                info += list_groups[count]
            else:
                info += list_groups[count] + ", "
            count += 1
        info += "\n"
    #Languages
    if len(list_languages) != 0:
        info += "Languages: "
        count = 0
        while count < len(list_languages):
            if count == len(list_languages)-1:
                info += list_languages[count]
            else:
                info += list_languages[count] + ", "
            count += 1
        info += "\n"
    #Categories
    if len(list_categories) != 0:
        info += "Categories: "
        count = 0
        while count < len(list_categories):
            if count == len(list_categories)-1:
                info += list_categories[count]
            else:
                info += list_categories[count] + ", "
            count += 1
        info += "\n"
    #Pages
    if len(list_pages) != 0:
        info += "Pages: "
        count = 0
        while count < len(list_pages):
            if count == len(list_pages)-1:
                info += list_pages[count]
            else:
                info += list_pages[count] + ", "
            count += 1
        info += "\n\n"

        info += "View more in " + url

def obtenerAtributos():
    obtenerTitulos()
    obtenerIdDoujinshi()
    obtenerIDGaleria()
    llenadoDeLista()
    llenadoDeListasDeAtributos()
    impresionDeListasAtributos()
    
def inicializaListas():
    global list_sections
    global list_parodies
    global list_characters
    global list_tags
    global list_artists
    global list_groups
    global list_languages
    global list_categories
    global list_pages
    
    list_sections = [False,False,False,False,False,False,False,False]
    list_parodies = list()
    list_characters = list()
    list_tags = list()
    list_artists = list()
    list_groups = list()
    list_languages = list()
    list_categories = list()
    list_pages = list()
        
def imprimeArchivo():
    global info
    if os.path.isdir('nhentai_xxx'):
        os.chdir('nhentai_xxx/')
        if os.path.isdir(doujinshi_id[1:]):
            if os.listdir(doujinshi_id[1:]):
                os.chdir(doujinshi_id[1:])
                if os.path.isfile("LEEME.txt"):
                    print("Ya existe el Archivo LEEME para el ID " + doujinshi_id[1:])
                    os.chdir('../../')
                else:
                    with open('LEEME.txt', 'w', encoding="utf-8") as f:
                        f.write(info)
                    os.chdir('../../')
            else:
                with open('LEEME.txt', 'w', encoding="utf-8") as f:
                    f.write(info)
                os.chdir('../../')
        else:
            os.mkdir(doujinshi_id[1:])
            os.chdir(doujinshi_id[1:] + '/')
            with open('LEEME.txt', 'w', encoding="utf-8") as f:
                f.write(info)
            os.chdir('../../')
    else:
        os.mkdir('nhentai_xxx')
        os.chdir('nhentai_xxx/')
        os.mkdir(doujinshi_id[1:])
        os.chdir(doujinshi_id[1:] + '/')
        with open('LEEME.txt', 'w', encoding="utf-8") as f:
            f.write(info)
        os.chdir('../../')
        
def descargaImagenes(lista_doujin):
    lista_aux = sorted(lista_doujin,key=itemgetter(2))
    for x in range(0,1):
        os.chdir('nhentai_xxx/')
        os.chdir(lista_aux[x][0])
        
        indice = 1
        print("Descargando imagenes para el ID #" + format(lista_aux[x][0]) + " (" + format(lista_aux[x][2]) + " imagenes)")
        while indice <= lista_aux[x][2]:
            #wget -b https://cdn.nhentai.xxx/g/1835710/{1..463}.jpg
            #wget -NS https://cdn.nhentai.xxx/g/1835710/1.jpg 2>&1 | grep "HTTP/" | awk '{print $2}'
            #wget --server-response https://cdn.nhentai.xxx/g/1835710/1.jpg 2>&1 | awk '/^  HTTP/{print $2}'

            valor = "%s" %indice
            print("Descargando " + valor + "/" + format(lista_aux[x][2]) + " imagenes \r")
            sys.stdout.flush()
            time.sleep(1)
            print("\r")
#            comando = 'wget -b https://cdn.nhentai.xxx/g/' + format(lista_aux[x][1]) + "/" + format(indice) + '.jpg'
#            os.system(comando)
            indice += 1
        os.chdir('../../')

def compruebaImagenes():
    global no_pag
    global gallery_id
    no_img = 1
    cadena = ""

    while no_img <= no_pag:
        cadena = format(no_img) + ".jpg"
        if not os.path.isfile(cadena):
            #print(cadena +  " YA EXISTE!!!")
            comando = 'wget https://cdn.nhentai.xxx/g/' + format(gallery_id[4]) + "/" + format(no_img) + '.jpg'
            os.system(comando)
        no_img += 1

def principal():
    global soup
    global atributos
    #Variables Globales
    global info
    global url
    global doujinshi_id
    global gallery_id
    global no_pag
    list_descargas = list()    
    
    fichero = open('Lista.txt')
    lineas = fichero.readlines()
    print("Generando archivos Leeme...")
    for linea in lineas:
        url = linea
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        atributos = soup.find_all('div', class_='tag-container field-name')
        inicializaListas()
        list_aux = list()
        obtenerAtributos()
        imprimeArchivo()
        list_aux.append(doujinshi_id[1:])
        list_aux.append(gallery_id[4])
        list_aux.append(no_pag)
        list_descargas.append(list_aux)
        info = ""
        
    print("\n Descargando imagenes...")
    descargaImagenes(list_descargas)
    fichero.close()
    
principal()
