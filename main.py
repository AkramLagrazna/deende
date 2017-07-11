# -*- coding: utf-8 -*-
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, request
#from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import  sessionmaker
import random
import requests
import datetime
from string import replace, strip
from datetime import datetime, timedelta
from database_setup import Base, User, Subito
import time
from statistics import mean

app = Flask(__name__)
Base = declarative_base()
engine = create_engine('sqlite:///subito.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
letters = ['a','b','c','d','e','f','g','h','i','l','m','n','o','p','q','r','s','t','u','v','w','y','k','z','1','2','3','4','5','6','7','8','9','0']


@app.route('/', methods = ['POST','GET'])
@app.route('/index', methods = ['POST','GET'])
def subito():

    prezzimedi = []
    titolisubito = []
    prezzisubito = []
    fotosubito = []
    postosubito = []
    titolikijiji = []
    prezzikijiji = []
    postokijiji = []

    #creare session_key
    global x, x
    random_lets = ['','','','','','','','','','','','','','','','','','','']
    vari = 10
    for x in range(1,vari):
        try:
            random_lets[x] = random.choice(letters)
        except IndexError:
            vari = x
    session_key = ''.join(random_lets)
    #reindirizza la richiesta se il method e post
    if request.method == 'POST':
        regione = request.form['regione']
        ricerca = request.form['ricerca']
        categoria = request.form['categoria']
        first_connection = requests.post("https://api.priceapi.com/jobs", json={
            "token": "FXTNOJUFAZBQMNACWBSMMVSKNFYDMKDBWGVZKBXXEITNONASJUGQEGJJVHHRBSEL",
            "country": 'it',
            "source": 'google-shopping',
            "currentness": 'daily_updated',
            'completeness': 'one_page',
            'key': 'keyword',
            'values': ricerca,
        })
        giaison = first_connection.json()

        response = requests.post("https://wrapapi.com/use/lagra/subitoapi/request_1/0.0.2", json={
          "wrapAPIKey": "vlOBFonN6t5xK5wQco5dXZ3NWnKzugH8",
          "regione" : regione,
          "ricerca" : ricerca,
          "categoria" : categoria
        })
        json = response.json()
        #algoritmo delle date
        output = '   '
        voro = 30
        lollie = ''
        try:
            try:
                for x in range(1,voro):
                    data = json['data']['quando'][x]['quandi']
                    giorna = []
                    for i in xrange(4):
                        giorna += data[i]
                    giorno = ''.join(giorna)
                    if giorno == 'Ieri':
                        orari = []
                        for p in range(6, 11):
                            orari += data[p]
                        my_dict = {}
                        orario = ''.join(orari)
                        orarii = datetime.strptime(orario, '%H:%M').time()
                        giornata = datetime.today() - timedelta(days=1)
                        dataseria = datetime.combine(giornata, orarii)
                        vor = 10
                        for z in range(1,vor):
                            try:
                                 my_dict[x] = Subito(
                                    titolo=json['data']['titoli'][x]['titolo'],
                                    prezzo=json['data']['prezzo'][x]['prezzi'],
                                    data=dataseria,
                                    foto=json['data']['collection'][x]['output'],
                                    posto=json['data']['citta'][x]['dove']
                                )
                                titolisubito[z] = json['data']['titoli'][z]['titolo']
                                prezzisubito[z] = json['data']['prezzo'][z]['prezzi']
                                fotosubito[z] = json['data']['collection'][z]['output']
                                postosubito[z] = json['data']['citta'][z]['dove']
                                annunciosubito[z] = str(titolisubito[z]) + ',' + str(prezzisubito[z]) + ',' + str(fotosubito[z]) + ',' + str(postosubito[z])
                                 #lollie += my_dict[x].prezzo
                            except IndexError:
                                vor = z
                        try:
                            if my_dict[x].prezzo == "Contattal'utente":
                                break
                            else:
                                lollie += my_dict[x].prezzo
                        except KeyError:
                            break
                    if giorno == 'Oggi':
                        orari = []
                        for p in range(6, 11):
                            orari += data[p]
                        my_dict = {}
                        orario = ''.join(orari)
                        orarii = datetime.strptime(orario, '%H:%M').time()
                        giornata = datetime.today()
                        dataseria = datetime.combine(giornata, orarii)
                        vor = 10
                        for z in range(1,vor):
                            try:
                                 my_dict[x] = Subito(
                                    titolo=json['data']['titoli'][x]['titolo'],
                                    prezzo=json['data']['prezzo'][x]['prezzi'],
                                    data=dataseria,
                                    foto=json['data']['collection'][x]['output'],
                                    posto=json['data']['citta'][x]['dove']
                                )
                                 #lollie += my_dict[x].prezzo

                            except IndexError:
                                vor = z
                        try:
                            if my_dict[x].prezzo == "Contattal'utente":
                                break
                            else:
                                lollie += my_dict[x].prezzo
                        except KeyError:
                            break
                kijiji = requests.post("https://wrapapi.com/use/lagra/italiakijiji/parser/0.0.1", json={
                    "wrapAPIKey": "vlOBFonN6t5xK5wQco5dXZ3NWnKzugH8",
                    "input": ricerca
                })
                jaison = kijiji.json()
                for x in range(1, voro):
                    datta = jaison['data']['quando'][x]['data']
                    giornaa = []
                    for i in xrange(4):
                        giornaa += datta[i]
                    giornoo = ''.join(giornaa)
                    if giornoo == 'Ieri':
                        orarii = []
                        for p in range(6, 11):
                            orarii += datta[p]
                        my_dicty = {}
                        orarioo = ''.join(orarii)
                        orariio = datetime.strptime(orarioo, '%H:%M').time()
                        giornataa = datetime.today() - timedelta(days=1)
                        dataseriaa = datetime.combine(giornataa, orariio)
                        vor = 20
                        for z in range(1, vor):
                            try:
                                my_dicty[x] = Subito(
                                    titolo=jaison['data']['titoli'][x]['titolo'],
                                    prezzo=jaison['data']['prezzi'][x]['prezzo'],
                                    posto=jaison['data']['dovi'][x]['dove']
                                )
                                #lollie += my_dicty[x].prezzo

                            except IndexError:
                                vor = z
                        try:
                            if my_dict[x].prezzo == "Contattal'utente":
                                break
                            else:
                                lollie += my_dicty[x].prezzo
                        except KeyError:
                            break
                    if giornoo == 'Ieri':
                        orarii = []
                        for p in range(6, 11):
                            orarii += datta[p]
                        my_dicty = {}
                        orarioo = ''.join(orarii)
                        orariio = datetime.strptime(orarioo, '%H:%M').time()
                        giornataa = datetime.today()
                        dataseriaa = datetime.combine(giornataa, orariio)
                        vor = 10
                        for z in range(1, vor):
                            try:
                                my_dicty[x] = Subito(
                                    titolo=jaison['data']['titoli'][x]['titolo'],
                                    prezzo=jaison['data']['prezzi'][x]['prezzo'],
                                    posto=jaison['data']['dovi'][x]['dove']
                                )

                                #lollie += my_dicty[x].prezzo

                            except IndexError:
                                vor = z
                        try:
                            if my_dict[x].prezzo == "Contattal'utente":
                                break
                            else:
                                lollie += my_dicty[x].prezzo
                        except KeyError:
                            break
            except IndexError:
                vor = x
        except TypeError:
            return "Nessun prodotto con quel nome! "


        wh = True
        while wh:
            second_connection = requests.get('https://api.priceapi.com/jobs/' + str(
                giaison['job_id']) + '?token=FXTNOJUFAZBQMNACWBSMMVSKNFYDMKDBWGVZKBXXEITNONASJUGQEGJJVHHRBSEL')
            giaisonn = second_connection.json()
            if giaisonn['status'] == 'finished':
                wh = False
                third_connection = requests.get('https://api.priceapi.com/products/bulk/' + str(
                    giaison['job_id']) + "?token=FXTNOJUFAZBQMNACWBSMMVSKNFYDMKDBWGVZKBXXEITNONASJUGQEGJJVHHRBSEL")
                finaljson = third_connection.json()
                prezzomedionuovo = finaljson['products'][0]['offers'][0]['price']
                wh = False
            else:
                wh = True
                time.sleep(5)
        words = lollie.replace(' €','+')
        newstring = words.replace('.', '')
        newarr = newstring.replace(' ', '')
        newarr = newarr[:-1]
        lol = eval(newarr)
        chiamare = newarr.strip('+')
        lunghezza = len(chiamare)
        mediafinale = lol / lunghezza
        return render_template('ricerca.html', output = my_dicty)
        #results = map(int, newarr)
        #return sum(results)
        #loan = str([w.replace('.','') for w in words])
        #loan = str([w.replace('u','') for w in words])



    if request.method == 'GET':
        return render_template('index.html')
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
