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
from datetime import datetime, timedelta
from statistics import mean
#finito importi
#creo applicazione Flask
app = Flask(__name__)
#creo array di lettere per la session_key
lettere = ['a','b','c','d','e','f','g','h','i','l','r','s','t','u','w','z','1','2','3','4','5','6','7']
#reindirizza alla home
@app.route('/', methods = ['POST','GET'])
@app.route('/index', methods = ['POST','GET'])
def subito():
    #creo session key
    random_lets = ['','','','','','','','','','','','','','','','','','','']
    vari = 10
    for x in range(1,vari):
        try:
            random_lets[x] = random.choice(lettere)
            
        except IndexError:
            vari = x
    session_key = ''.join(random_lets)
    #reindirizza la richiesta se è in GET
    if request.method == 'GET':
        ora = datetime.now()
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
        response = requests.post("https://wrapapi.com/use/lagra/subitoapi/request_1/0.0.2", json={
          "wrapAPIKey": "vlOBFonN6t5xK5wQco5dXZ3NWnKzugH8",
          "regione" : regione,
          "ricerca" : ricerca,
        })
        #json della richiesta dello scraper di subito.it
        json = response.json()
        #ora si presenta un problema
        #nel json la data viene rappresentata dal giorno, e poi dall'ora
        #quindi devo scrivere del codice per convertirlo in orario supportato da python
        annuncii = 30
        for x in range(1,annuncii):
            try:
                data = json['data']['quando'][x]['quandi']
                giorna = []
                for i in xrange(4):
                    giorna += data[i]
                #il risultato di giorno sarà 'Ieri' o 'Oggi'
                giorno = ''.join(giorna)
                if giorno == 'Ieri':
                    orari = []
                    for p in range(6,11):
                        #prendo solo l'orario
                        orari += data[p]
                    orariooo = ''.join(orari)
                    orarii = datetime.strptime(orariooo, '%H:%M').time()
                    giornata = datetime.today() - timedelta(days=1)
                    dataseria = datetime.combine(giornata, orarii)
                    date[x] = dataseria
                if giorno == 'Oggi':
                    orari = []
                    for p in range(6,11):
                        #stessa cosa
                        orari += data[p]
                    orariooo = ''.join(orari)
                    orarii = datetime.strptime(orariooo, '%H:%M').time()
                    giornata = datetime.today()
                    dataseria = datetime.combine(giornata, orarii)
                    date[x] = dataseria
            except IndexError:
                annuncii = x
        #ora aggiunge ad  un array tutte le date per ordine di annuncio
        ancoraannunci = 30
        for z in range(1,ancoraannunci):
            try:
                titolisubito[z] = json['data']['titoli'][z]['titolo']
                prezzisubito[z] = json['data']['prezzo'][z]['prezzi']
                fotosubito[z] = json['data']['collection'][z]['output']
                postosubito[z] = json['data']['citta'][z]['dove']
                annunciosubito[z] = str(titolisubito[z]) + ',' + str(prezzisubito[z]) + ',' + str(fotosubito[z]) + ',' + str(postosubito[z])

            except IndexError:
                ancoraannunci = z
        output = ''
        for titolo in titolisubito:
            output += titolo
        return output



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
