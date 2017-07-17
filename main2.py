# -*- coding: utf-8 -*-
# encoding=utf-8
import sys
reload(sys)
#configuro l'encoding dei caratteri su utf-8 su sys
sys.setdefaultencoding('utf-8')
#importo tutte le dipendenze
from flask import Flask, render_template, request
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import random, requests, time
from string import replace, strip
import datetime
from datetime import  timedelta
from statistics import mean
app = Flask(__name__)
lettere = ['a','b','c','d','e','f','g','h','i','l','r','s','t','u','w','z','1','2','3','4','5','6','7']
class Annuncio():
    def __init__(self, ranking):
        self.ranking = int(ranking )
#reindirizza alla home
@app.route('/', methods = ['POST','GET'])
@app.route('/index', methods = ['POST','GET'])
def subito():
    #reindirizza la richiesta se e in GET
    if request.method == 'GET':
        ora = datetime.datetime.now()
        return render_template('index.html')
    #reindirizza la richiesta se è in POST
    if request.method == 'POST':
        date = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
       #prendi dati dal form
        regione = request.form['regione']
        ricerca = request.form['ricerca']
        #effettuo prima connessione alla api di priceapi.com che mi da il prezzo nuovo del prodotto
        first_connection = requests.post("https://api.priceapi.com/jobs", json={
            "token": "FXTNOJUFAZBQMNACWBSMMVSKNFYDMKDBWGVZKBXXEITNONASJUGQEGJJVHHRBSEL",
            "country": 'it',
            "source": 'google-shopping',
            "currentness": 'daily_updated',
            'completeness': 'one_page',
            'key': 'keyword',
            'values': ricerca,
        })
        #json della risposta
        giaison = first_connection.json()
        #ho già costruito un api che fa da scraper su subito.it , ora mi devo solo connettere
        response = requests.post("https://wrapapi.com/use/lagra/subitoparse/parsubito/0.0.2", json={
          "wrapAPIKey": "vlOBFonN6t5xK5wQco5dXZ3NWnKzugH8",
          "regione" : regione,
          "ricerca" : ricerca,
        })
        #json della richiesta dello scraper di subito.it
        json = response.json()
        annuncii = 30
        orarisubi = ''
        prezzisubi = ''
        titolosubi = ''
        postosubi = ''
        for x in range(1,annuncii):
            try:
                data = json['data']['quandi'][x]['quando']
                prezzo = json['data']['prezzi'][x]['prezzo']
                titolo = json['data']['titoli'][x]['titolo']
                dove = json['data']['dovi'][x]['dove']
                giorna = []
                for i in xrange(4):
                    giorna += data[i]
                #il risultato di giorno sarà 'Ieri' o 'Oggi'
                giorno = ''.join(giorna)
#                if giorno == 'Ieri':
#                    for p in range(6,11):
#                        #prendo solo l'orario
#                        orari += data[p]
#                    orariooo = ''.join(orari)
                if giorno == 'Oggi':
                    for p in range(6,11):
                        #stessa cosa
                        orarisubi += data[p]
                    orarisubi += ';'
                    prezzisubi += prezzo
                    prezzisubi += ';'
                    titolosubi += titolo
                    titolosubi += ';'
                    postosubi += dove
                    postosubi += ';'
            except IndexError:
                annuncii = x
        #strippare prezzi e creare array per tutti i fattori dell'annuncio
        #.split per fare arrays
        prezzisubii = prezzisubi.replace("€", "")
        prezzisubit = prezzisubii.replace(" ", "")
        #creato array prezzi subito
        prezzisubitoo = prezzisubit.replace(".", "")
        prezzisubito = prezzisubitoo.split(';')
        titolosubito = prezzisubi.split(';')
        postosubito = postosubi.split(';')
        orarisubito = orarisubi.split(';')
        #creare la stessa cosa per kijiji
        risposta = requests.post("https://wrapapi.com/use/lagra/italiakijiji/parser/0.0.1", json={
          "wrapAPIKey": "vlOBFonN6t5xK5wQco5dXZ3NWnKzugH8",
          "regione" : regione,
          "ricerca" : ricerca,
        })
        #json della richiesta dello scraper di subito.it
        jsonn = risposta.json()
        annuncii = 30
        orarikiji = ''
        prezzikiji = ''
        titolokiji = ''
        postokiji = ''
        for x in range(1,annuncii):
            try:
                data = jsonn['data']['quando'][x]['data']
                #if data.find('tatta') == -1:
                #    pass
                prezzo = jsonn['data']['prezzi'][x]['prezzo']
                titolo = jsonn['data']['titoli'][x]['titolo']
                dove = jsonn['data']['dovi'][x]['dove']
                giorna = []
                for i in xrange(4):
                    giorna += data[i]
                #il risultato di giorno sarà 'Ieri' o 'Oggi'
                giorno = ''.join(giorna)
#                if giorno == 'Ieri':
#                    for p in range(6,11):
#                        #prendo solo l'orario
#                        orari += data[p]
#                    orariooo = ''.join(orari)
                if giorno == 'Oggi':
                    for p in range(6,11):
                        #stessa cosa
                        orarikiji += data[p]
                    orarikiji += ';'
                    prezzikiji += prezzo
                    prezzikiji += ';'
                    titolokiji += titolo
                    titolokiji += ';'
                    postokiji += dove
                    postokiji += ';'
            except IndexError:
                annuncii = x


        #strippare prezzi e creare array per tutti i fattori dell'annuncio
        #.split per fare arrays
        prezzikijii = prezzikiji.replace("€", "")
        prezzikijij = prezzikijii.replace(" ", "")
        prezzikijijii = prezzikijij.replace(".", "")
        prezzikijiji = prezzikijijii.split(';')
        titolokijiji = prezzikiji.split(';')
        postokijiji = postokiji.split(';')
        orarikijiji = orarikiji.split(';')

        #mettere tutto piu array
        #indice di credibilita
        #fare la media
        #confronta media usato con media nuovo e prendi 10 annunci credibili
        #contronta quelli
        #ouputta il migliore
        #bella grafica e
        outputt = ''
        for x in titolokijiji:
            outputt += x
        return outputt

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
