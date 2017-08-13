# -*- coding: utf-8 -*-
# encoding=utf-8
import sys
reload(sys)
#configuro l'encoding dei caratteri su utf-8 su sys
sys.setdefaultencoding('utf-8')
#importo tutte le dipendenze
from flask import Flask, render_template, request
import random, requests, time
from string import replace, strip
import datetime
from datetime import  timedelta
import statistics as s
app = Flask(__name__)
lettere = ['a','b','c','d','e','f','g','h','i','l','r','s','t','u','w','z','1','2','3','4','5','6','7']
class Annuncio(object):
    titolo = ''
    prezzo = 0
    posto = ''
    orario = ''
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
        response = requests.post("https://wrapapi.com/use/lagra/subitoparse/parsubito/latest", json={
          "wrapAPIKey": "vlOBFonN6t5xK5wQco5dXZ3NWnKzugH8",
          "regione" : regione,
          "ricerca" : ricerca,
        })
        #json della richiesta dello scraper di subito.it
        json = response.json()
        annuncii = 26
        orarisubi = ''
        prezzisubi = ''
        titolosubi = ''
        postosubi = ''
        for x in range(1,annuncii):
            try:
                data = json['data']['quandi'][x]['quando']
                prezzo = json['data']['prezzi'][x]['prezzo']
                titoloo = json['data']['titoli'][x]['titolo']
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
                    titolosubi += titoloo
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
        titolosubito = titolosubi.split(';')
        postosubito = postosubi.split(';')
        orarisubito = orarisubi.split(';')
        #quindi ora ho quattro array. "PrezziSubito", "TitoloSubito", "PostoSubito" ed "OrariSubito"

        #creare la stessa cosa per kijiji
        rispostq = requests.post("https://wrapapi.com/use/lagra/italiakijiji/parser/latest", json={
          "wrapAPIKey": "vlOBFonN6t5xK5wQco5dXZ3NWnKzugH8",
          "input" : ricerca,
        })
        #json della richiesta dello scraper di subito.it
        jsonn = rispostq.json()
        annuncii = 26
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
        titolokijiji = titolokiji.split(';')
        postokijiji = postokiji.split(';')
        orarikijiji = orarikiji.split(';')
        #ora ho Quattro altri array "PrezziKijiji", "TitoloKijiji" , "PostoKijiji" e "OrariKijiji"
        #sommare gli arrays
        listaprezzi= prezzisubito + prezzikijiji
        listatitoli = titolosubito + titolokijiji
        listaposti = postosubito + postokijiji
        listaorari = orarisubito + orarikijiji
        #fare la media
        listaprezzi = listaprezzi[:-2]
        try:
            total = reduce(lambda acc, x: float(acc) + (float(x) if x else 0),listaprezzi,0)
            length = reduce(lambda acc, x: float(acc) + (1 if x else 0),listaprezzi,0)
            average = (',',total/length)[length > 0]
            return str(average)
        except ZeroDivisionError:
            pass
            #non ci sono ancora annunci
        #indice di credibilita
        numero = 0
        numerobuono = 0
        annuncibuoni = []
        lunghezza = len(listatitoli)
        for numera in xrange(1, lunghezza):
            annuncio = Annuncio(numero)
            annuncio.titolo = listatitoli[numero]
            annuncio.prezzo = listaprezzi[numero]
            annuncio.posto = listaposti[numero]
            annuncio.orario = listaorari[numero]
            titoloannuncio = annuncio.titolo
            if ricerca.find('cover') != -1 or ricerca.find('carica') != -1 or ricerca.find('custodia', 40) != -1 or titoloannuncio.find('mouse', 40) != -1:
                annuncio.ranking = annuncio.ranking - 10
            else:
                #keyword presente nella ricerca
                annuncio.ranking = annuncio.ranking + 1
                pass
            if ricerca.find('alimentatore', 40) != -1 or ricerca.find('effetto', 40) != -1 or ricerca.find('adattatori', 40) != -1:
                annuncio.ranking = annuncio.ranking - 10
            else:
                #keyword presente nella ricerca
                annuncio.ranking = annuncio.ranking + 1
                pass
            #parole dannose
            if titoloannuncio.find('non funziona', 40) != -1 or titoloannuncio.find('rotto', 40) != -1 or titoloannuncio.find('danneggiato', 40) != -1:
                annuncio.ranking = annuncio.ranking - 20
            #parole buone
            if titoloannuncio.find('funziona', 40) != -1 or titoloannuncio.find('ram', 40) != -1 or titoloannuncio.find('nuovo', 40) != -1:

                annuncio.ranking = annuncio.ranking + 10
            if annuncio.ranking >= 0:
                annuncibuoni[numerobuono] = str(numero)
            numero = numero + 1
        #prendi annunci credibili 
        prezzicredibili = []
        titolicredibili = []
        posticredibili = []
        oraricredibili = []
        numeroooo = 0
        for annunciobuono in annuncibuoni:
            en = int(annunciobuono)
            prezzicredibili[numeroooo] = listaprezzi[en]
            titolicredibili[numeroooo] = listatitoli[en]
            posticredibili[numeroooo] = listaposti[en]
            oraricredibili[numeroooo] = listaorari[en]
        #confronta media usato con media nuovo e prendi 10 annunci credibili
        job_id = giaison['job_id']
        pronto = False
        while pronto == False:
            second_connection = requests.get('https://api.priceapi.com/jobs/' + str(job_id) + '?token=FXTNOJUFAZBQMNACWBSMMVSKNFYDMKDBWGVZKBXXEITNONASJUGQEGJJVHHRBSEL')
            jaa = second_connection.json()
            if jaa['status'] == 'finished':
                pronto = True
            else:
                pronto = False
        third_connection = requests.get('https://api.priceapi.com/products/bulk/' + str(job_id) + '?token=FXTNOJUFAZBQMNACWBSMMVSKNFYDMKDBWGVZKBXXEITNONASJUGQEGJJVHHRBSEL')
        jsson = third_connection.json()
        prezzo_nuovo = jsson['products'][0]['offers'][0]['price']
        nanmero = 0
        for annuncista in prezzicredibili:
            xx = (prezzo_nuovo * 34) / 100
            if xx < annuncista:
                del prezzicredibili[nanmero]
                del titolicredibili[nanmero]
                del oraricredibili[nanmero]
                del posticredibili[nanmero]
            try: 
                lol = int(annuncista) / 4
                if lol < average:
                    del prezzicredibili[nanmero]
                    del titolicredibili[nanmero]
                    del oraricredibili[nanmero]
                    del posticredibili[nanmero]
            except Exception: 
                pass
        return render_template('ricerca.html ', prezzicredibili = prezzicredibili , )

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)

