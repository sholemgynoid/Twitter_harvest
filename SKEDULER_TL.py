#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Passi di: Matthew A. Russell. “Mining the Social Web”. iBooks.

import time
import pdb
import config

from Harvest_User_Timeline import FETCH_USER_TIMELINE
from RICERCA_TWIT_CON_CHIAVI import RICERCA_TL_CON_CHIAVI
from CHECK_RATE_LIMIT_STATUS import CHECK_RATE_LIMIT_STATUS
from funzioni_supporto import *
from IMPORT_DOCS import CONNECT_MONGODB
from IMPORT_DOCS import CREATE_INDEX

db = input('db: ')
collection = input('Collezione: ')
config.indice_account_dev = int(input('Indice account dev: '))

mydb = CONNECT_MONGODB(db , collection)
CREATE_INDEX(mydb , "id" , "id_tweet" , True)

dati_ricerca = []
numero_twit_ultima_ricerca = 0

t_ricerca = [0 , 0 , 0]
tweet_ricerca = [0 , 0 , 0]
ultime_ricerche_residue = [180 , 0]
t_hour = 3600

#  Qui sotto si mettono gli account dei politici 
#  tra apici.   
#  non dimeticare la virgola. Dopo l'ultimo non ci va la virgola.
#  Quando hai finito, scrivi che controllo e avvio

q = [
    'ellyesse' ,
    'pfmajorino' ,			#Candidato Regione Lombardia
    'ciriani_luca' ,		#Ministro
    'SimoPillon' ,
    'EnricoLetta' ,			#Segretario PD
    'Ettore_Rosato' ,		#Deputato Presidente #ItaliaViva
    'RicRicciardi' ,		#Portavoce Camera dei Deputati MoVimento 5 Stelle
    'NotizieFrance' ,		#Francesco Emilio Borrelli portavoce Europa verde
    'marattin' ,			#Presidente della Commissione Finanze della Camera IV
    'rugge75' ,				#Andrea Ruggieri Deputato di FI Non attivo
    'emanuelefiano' ,		#Deputato PD
    'gennaromigliore' ,		#Deputato IV
    'emmabonino' ,			#Senatrice +E
    'Ignazio_LaRussa' ,		#Presidente Camera
    'LetiziaMoratti' ,		#Assessora Lombardia CDX
    'Pierferdinando' ,		#Deputato Misto
#    'luigidimaio' ,
    'CarloCalenda' ,
    'grotondi' ,
    'Maurizio_Lupi' ,
    'RaffaeleFitto' ,
    'marioadinolfi' ,
    'Storace' ,
    'GiorgiaMeloni' ,
#    'renatobrunetta' ,		#Governo FI ACCOUNT PROTETTO
    'szampa56' ,			#responsabile Dipartimento Salute Pd
    'VeriniWalter' ,		#Deputato Partito Democratico Capogruppo PD Comm Giustizia
    'gasparripdl' ,
    'GiovanniToti' ,
#    'Ale_Mussolini_' ,
    'renatapolverini' ,
    'mara_carfagna' ,		#Governo FI
    'Antonio_Tajani' ,
    'DeborahBergamin' ,
    'lauraravetto' ,
    'matteorenzi' ,
    'robertapinotti' ,
    'dariofrance' ,
    'PaoloGentiloni' ,
    'graziano_delrio' ,
    'bealorenzin' ,
    'meb' ,
    'LottiLuca' ,
    'ivanscalfarotto' ,
#    'SteGiannini' ,
#    'maumartina' ,
    'lauraboldrini' ,
#    'PietroGrasso' ,
    'matteosalvinimi' ,
    'edorixi' ,
    'giamma71' ,			#Governo Lega
    'erikastefani71' ,		#Governo Lega
    'beppe_grillo' ,
    'ale_dibattista' ,
    'PaolaTavernaM5S' ,
    'Roberto_Fico' ,		# M5s
    'pbersani' ,
    'serracchiani' ,
    'guerini_lorenzo' ,		# IV
#    'erealacci' ,
    'robersperanza' ,
    'rossipresidente' ,
#    'civati' ,
    'demagistris' ,
    'NFratoianni' ,
    'StefanoFassina' ,
    'borghi_claudio' ,
#    'giulianopisapia' ,
    'virginiaraggi' ,
    'c_appendino' ,
    'fralaforgia' ,
    'AndreaOrlandosp' ,
    'berlusconi' ,
    'giorgio_gori' ,
    'dariovioli' ,
    'robertalombardi' ,
    'orfini' ,
    '_paolo_romani_' ,
    'DaniloToninelli' ,
    'ViolaCarofalo' ,
    'msgelmini' ,
    'Fontana3Lorenzo' ,
#    'vincenzozoccano' ,
#    'LucianoBarraCar' ,
#    'ecdelre' ,
    'ManlioDS' ,
    'RicardoMerlo5' ,
    'CandianiStefano' ,
    'LuigiGaetti' ,
    'NicolaMolteni' ,
    'carlosibilia' ,
    'AlfonsoBonafede' ,
    'Ferraresi_V' ,
    'JacopoMorrone' ,
    'Eli_Trenta' ,
    'AngeloTofalo' ,
    'volpi_raffaele' ,
    'massimobitonci' ,
#     'LaCastelliM5s' ,
    'massimogara' ,
    'ale_villarosa' ,
#    'AlePesce_mipaaf' ,
#    'SergioCosta_min' ,
#    'Quirinale' ,
    'VanniaGava' ,
    'micillom5s' ,
#    'dellorco85' ,
    'edorixi' ,
    'armandosiri' ,
    'cla_cominardi' ,
    'ClaudioDurigon' ,
#    'bussetti_marco' ,
    'lofioramonti' ,
#    'giulianosal' ,
#    'BonisoliAlberto' ,
    'GianlucaVacca' ,
    'LuciaBorgonzoni' ,
    'GiuliaGrilloM5S' ,
    'MaurizioFugatti' ,
    'GiuseppeConteIT' ,
    'VeltroniWalter' ,		#Esponente PD
    'vitocrimi' ,
    'riccardo_fra' ,		#Deputato M5s
    'ValenteM5S' ,
    'gbongiorno66' ,
    'MFantinati' ,
    'SBuffagni' ,
    'DanielePesco' ,
    'AlbertoBagnai' ,
#    'carlaruocco1' ,
    'GianniGirotto' ,
    'CatalfoNunzia' ,
    'BSaltamartini' ,
    'BorghesiStefano' ,
    'g_brescia' ,
    'GiuliaSarti86' ,
    'AndreaOstellari' ,		#Senatore Lega
    'LuigiGallo15' ,
    'vitopetrocelli' ,
    'MartaGrande87' ,
    'ettore_licheri' ,		#Senatore M5s
    'vilmamoronese' ,
    'alebenvenuto' ,
    'Gallinella_F' ,
    'AndreaMarcucci' ,
    'fabiorampelli' ,
    'BertaccoS' ,
    'Fornaro62' ,
    'roccocasalino',
    'bendellavedova',
#    'ceriscioliluca' ,
    'g_falcomata' ,
    'mattpalazzi' ,
    'drmk73' ,
    'arturolorenzoni' ,
    'FabrizioFracas3' ,
    'LauCastelletti' ,
    'stefanoballeari' ,
    'aless_andre' ,
#    'marioguarente' ,
    'GravinaRoberto' ,
    'fulviocentoz' ,
#    'Mov5Stelle' ,
    'BaldinoVittoria' ,
#    'EnricoMichetti' ,
#    'lorusso_stefano' ,
#    'virginiomerola' ,
#    'GaeManfredi' ,
    'RobertoDipiazza' ,
    'DadoneFabiana' ,
#    'elenabonetti' ,		#Governo IV
    'giorgiomule' ,			#Governo FI
    'Nello_Musumeci' ,		#Ministro
    'RaffaeleFitto' ,		#Ministro
    'andreaabodi' ,			#Ministro
    'Piantedosim' ,			#Ministro
    'BerniniAM' ,			#Ministra
    'GuidoCrosetto' ,		#Ministro
    'Min_Casellati' ,		#Ministra
    'adolfo_urso' ,			#Ministro
    'ciriani_luca' ,		#Ministro
    'DSantanche' ,			#Ministra
    'G_Valditara' ,			#Ministro
    'Ale_Locatelli_' , 		#Alessandra Locatelli - Ministra
    'augustamontarul' ,		#Deputata FDI
    'DantiNicola' ,			#Parlamento Ue IV
    'itinagli' ,			#Parlamento Ue PD
#    'massimogara' ,
    'GoffredoBettini' ,
    'LucioMalan' ,
    'EGardini' ,
    'ylucaselli' ,
    'AnnaAscani' ,
    'ZanAlessandro' ,
    'LiaQuartapelle' ,
    'aleCattaneo79' ,
    'piersileri' ,
    'FrancescoLollo1' ,		#Ministro
    'MolinariRik' ,
    'davidefaraone' ,
    'antoniomisiani' ,
    'Donzelli' ,
    'maxromeoMB' ,
    'peppeprovenzano' ,
    'CostaAndrea70' ,
    'brandobenifei' ,		#Capodelegazione PD al Parlamento Europeo
    'LiciaRonzulli' ,		#Senatore FI Presidente della Commissione bicamerale infanzia
    'FloridiaBarbara' ,		#Portavoce M5s Senato
    'dariogalli5' ,			#Deputato Lega
    'CandianiStefano' ,		#Senatore Lega
    'SimonaMalpezzi' ,		#Presidente dei @senatoripd
    'PetrisDe' ,			#Senatrice Presidente Gruppo Misto e Sinistra Italiana
    'DelmastroAndrea' ,		#Deputato e responsabile Esteri di FratellidItalia
    'FidanzaCarlo' ,		#Deputato di Fratelli d'Italia - ECR al Parlamento Europeo
    'Pinokabras' ,			#Deputato Alternativa
    'AcquaroliF' ,			#Presidente Regione Marche FDI
    'Alberto_Cirio' ,		#Presidente Regione Piemonte FI
    'ArnoKompatscher' ,		#Presidente TAA SVP
    'ChristianSolin3' ,		#Presidente Regione Sardegna PSDAZ Non attivo
    'Donatella_Tesei' ,		#Presidente Regione Umbria Lega Non attivo
    'ErikLavevaz' ,			#Presidente Regione VDA UV
    'EugenioGiani' ,		#Presidente Regione Toscana PD
    'FontanaPres' ,			#Presidente Regione Lombardia Lega
    'M_Fedriga' ,			#Presidente Regione FVG Lega
    'marcomarsilio' ,		#Presidente Regione Abruzzo FDI
    'micheleemiliano' ,		#Presidente Regione Puglia PD
    'nzingaretti' ,			#Presidente Regione Lazio PD
    'robertoocchiuto' ,		#Presidente Regione Calabria FI
    'sbonaccini' ,			#Presidente Regione ER PD
    'TomaDonato' ,			#Presidente Regione Molise FI Non attivo
    'VincenzoDeLuca' ,		#Presidente Regione Campania PD
    'VitoBardi' ,			#Presidente Regione Basilicata FI
    'zaiapresidente' ,		#Presidente Regione Veneto Lega
    'RenatoSchifani' ,		#Presidente Regione Sicilia
    'Andrea_Romizi' ,		#Sindaco Perugia FI
    'Antonio_Decaro' ,		#Sindaco Bari PD
    'BeppeSala' ,			#Sindaco Milano EV
    'buccipergenova' ,		#Sindaco Genova Altri
    'DarioNardella' ,		#Sindaco Firenze PD
    'gualtierieurope' ,		#Sindaco Roma PD
    'fiane' ,				#Sindaco Trento CSX
    'GaeManfredi' ,			#Sindaco Napoli CSX
    'GravinaRoberto' ,		#Sindaco Campobasso M5s
    'robertolagalla' ,		#Sindaco Palermo PD
    'lorusso_stefano' ,		#Sindaco Torino CSX
    'LuigiBrugnaro' ,		#Sindaco Venezia Coraggio Italia
    'marioguarente' ,		#Sindaco Potenza Lega nord
    'nuti_g' ,				#Sindaco Aosta Indipendente
    'PierluigiBiondi' ,		#Sindaco Aquila FDI
    'RobertoDipiazza' ,		#Sindaco Trieste FI
    'SergioAbramo' ,		#Sindaco Catanzaro Coraggio Italia
    'truzzu' ,				#Sindaco Cagliari FDI
    'matteolepore' ,		#Sindaco Bologna PD
    'MattBiff' ,			#Sindaco Prato PD
    'matteoricci' ,			#Sindaco Pesaro PD
    'EleonoraEvi' ,			#Portavoce Europa Verde
    'CottarelliCPI' ,		#Candidat* 2022
    'aboubakar_soum'		#Candidat* 2022
    ]

try:
    with open("_count.txt" , "r"):
        pass
except IOError:
    print("creo file di servizio...")
    f_count = open("_count.txt" , "w")
    f_count.write("0")
    f_count.close()

    f_since = open("_since_id.txt" , "w")
    f_since.write("1")
    f_since.close()

i = 1

while True:

    f_since_id = open('_since_id.txt' , 'r')
    since_id = f_since_id.read()
    f_since_id.close()
    print('f_since_id - since_id: {}'.format(since_id))

    f_count = open('_count.txt' , 'r')
    contatore = f_count.read()
    f_count.close()

    for user_name in q:

        semaforo_scrittura_since_id = (i == 1)

        print ('avvio ricerca con chiave {} - Ciclo {} - Ciclo soggetto {}'.format(user_name , contatore , i))
        #     try:

        print ('VALORE DEL SEMAFORO SCRITTURA: {}; VALORE DEL SEMAFORO GLOBALE: {}'.format(semaforo_scrittura_since_id ,
                                                                                          config.semaforo_globale))

        print ('since_id: ' + since_id)

        numero_twit_ultima_ricerca = FETCH_USER_TIMELINE(since_id , contatore , i , user_name ,
                                                         (semaforo_scrittura_since_id or config.semaforo_globale) ,
                                                         mydb)

        #     except:
        #         numero_twit_ultima_ricerca = 0

        # dati_ricerca = CHECK_RATE_LIMIT_STATUS()

        print('data e ora: {}'.format(time.strftime("%a, %d %b %Y %H:%M:%S +0000" , time.gmtime())))

        print('FINE')
        print('contatore: ' + contatore)

        if contatore == '0':
            time.sleep(900)
        else:
            time.sleep(300)

        #         print 'Attendo 900 secondi prima della prossima ricerca...'

        i = i + 1  # Aumento di 1 il contatore degli account da scaricare

    i = 1  # Resetto il contatore degli account da scaricare, per il prossimo ciclo

    if not config.semaforo_globale:
        f_since_id = open('_since_id.txt' , 'w')
        f_since_id.write(config.since_id_new)
        f_since_id.close()

    config.semaforo_globale = True
    config.max_id_new = '1'

    print('********** AGGIORNO FILE _count.txt')

    f_count = open('_count.txt' , 'w')
    f_count.write(str(int(contatore) + 1))
    f_count.close()

    pause = t_hour * 4

    print('********** RIATTIVAZIONE PROCESSO TRA {} secondi'.format(pause))

    time.sleep(pause)
