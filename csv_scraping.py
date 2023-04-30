import csv
import codecs
from selenium import webdriver
from bs4 import BeautifulSoup

if __name__ == '__main__':
    pathCSVAziende = "./aziende.csv"
    pathCSVCompleto = "./aziende_telefono.csv"

    #apro il browser
    driver = webdriver.Firefox()
    #Creo il file dove andranno salvate le informazioni
    f = open(pathCSVCompleto, 'w')
    with open(pathCSVAziende, 'r') as file:
        csvreader = csv.reader(file)
        #for che cicla per ogni riga del csv di partenza
        for row in csvreader:
            URL = row[0]
            #navigo verso l'URL appena letto
            driver.get(URL)
            #prendo il dom della pagina html caricata
            html = driver.page_source
            #decode in HTML 
            soup = BeautifulSoup(html, 'html.parser')
            #extract data -> prendo tutti i div con classe "vc_column-inner" 
            externDiv = soup.find("div", {"class":"vc_column-inner"})
            #prendo tutti i div contnuti in externalDiv
            innerDiv = externDiv.find_all("div")
            for div in innerDiv:
                #le informazioni non hanno tag, id o classi specifiche quindi leggo il testo della label sopra 
                lbl = div.find("label")
                #se la label esiste e il suo contenuto è "Telefono"
                if lbl and lbl.string == "Telefono":
                    #leggo il numero di telefono dal div sottostante (il tag successivo nel dom)
                    telefono = lbl.findNext('div').string
                    #preparo e scrivo la riga nel CSV
                    row = URL+","+str(telefono)+"\n"
                    f.write(row)

    #chiudo il file di scrittura e il browser
    f.close()
    driver.close()