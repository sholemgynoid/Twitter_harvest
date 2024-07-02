#!/usr/bin/python
# -*- coding: utf-8 -*-
#  Passi di: Matthew A. Russell. “Mining the Social Web”. iBooks. 

# from __future__ import print_function

import io
import time
from http.client import BadStatusLine
from urllib import error

import twitter as tw

from IMPORT_DOCS import *


def harvest_user_timeline(since_id , i , semaforo , twitter_api , screen_name=None , user_id=None , max_results=3200):
    print('Valore di SEMAFORO GLOBALE dentro la funzione harvest_user_timeline: {}'.format(config.semaforo_globale))
    print('harvest_user_timeline - since_id: {}'.format(since_id))

    assert (screen_name != None) != (user_id != None) , "Must have screen_name or user_id, but not both"

    print('********** {}'.format(str(semaforo)))

    # setting delle keyword per la chiamata alle API di Twitter

    if ((i == 1) or (config.max_id_new == "1")):

        kw = {
            'count': 200 ,
            # 'trim_user': 'true',
            'include-rts': 'true' ,
            'since_id': since_id ,
            'tweet_mode': 'extended'
        }

    else:

        kw = {
            'count': 200 ,
            # 'trim_user': 'true',
            'include-rts': 'true' ,
            'since_id': since_id ,
            'max_id': config.max_id_new ,
            'tweet_mode': 'extended'
        }

    # 	'trim_user':
    #	When set to either true, t or 1, each tweet returned in a timeline
    # 	will include a user object including only the status authors numerical ID.
    # 	Omit this parameter to receive the complete user object.

    # 	'include-rts':
    #	When set to either true, t or 1,the timeline will contain native retweets
    # 	(if they exist) in addition to the standard stream of tweets.
    # 	The output format of retweeted tweets is identical to the representation
    # 	you see in home_timeline.
    # 	Note: If you're using the trim_user parameter in conjunction with include_rts,
    # 	the retweets will no longer contain a full user object.

    if screen_name:
        kw['screen_name'] = screen_name
    else:
        kw['user_id'] = user_id

    print(kw)

    max_pages = 16

    results = []

    tweets = make_twitter_request(twitter_api.statuses.user_timeline , **kw)

    if tweets is None:
        tweets = []

    #	Se la "pescata" ha avuto esito positivo e è il primo giro, oppure se il max_id è ancora uguale a 1, aggiorno il max_id
    #	Aggiungo anche la voce 'max_id' alla query dei tweet, in modo che la query si fermi al tweet più grande pescato nel primo giro

    if (len(tweets) > 0) and ((i == 1) or (config.max_id_new == "1")):
        config.max_id_new = str(max([tweet['id'] for tweet in tweets]))
        config.since_id_new = str(max([tweet['id'] for tweet in tweets]) + 1)

        print('********** NUOVO MAX SINCE_ID = {}'.format(config.since_id_new))

        config.semaforo_globale = False

        kw['max_id'] = config.max_id_new

    results += tweets

    # 	print >> sys.stderr, 'Fetched %i tweets' % len (tweets)

    page_num = 1

    if max_results == kw['count']:
        page_num = max_pages

    while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:
        kw['max_id'] = min([tweet['id'] for tweet in tweets]) - 1

        tweets = make_twitter_request(twitter_api.statuses.user_timeline , **kw)

        results += tweets

        # 		print >> sys.stderr, '********** FETCHED %i TWEETS' % len(tweets)

        page_num += 1

    print ('Done fetching tweets', file=sys.stderr)

    print('********** RECUPERATI {} TWEET*****'.format(len(results)))

    return results[:max_results]


def make_twitter_request(twitter_api_func , max_errors=10 , *args , **kw):
    def handle_twitter_http_error(e , wait_period=2 , sleep_when_rate_limited=True):

        if wait_period > 3600:
            print ('too many retries -> Quitting', file=sys.stderr)
            raise e

        if e.e.code == 401:

            print ('Encountered 401 Error (Not authorized)', file=sys.stderr)
            return none

        elif e.e.code == 404:

            print('Encountered 404 Error (Not found)', file=sys.stderr)
            return None

        elif e.e.code == 429:

            print ('Encountered 429 Error (Rate limit exceeded)', file=sys.stderr)

            if sleep_when_rate_limited:

                print ('Retrying in 15 minutes... ZzZ...', file=sys.stderr)
                sys.stderr.flush()
                time.sleep(60 * 15 + 5)
                print ('ZzZ... Awake now and trying again.', file=sys.stderr)
                return 2

            else:

                raise e

    wait_period = 2
    error_count = 0

    while True:

        try:
            # 			print 'PROVO A CERCARE I TWEET'
            return twitter_api_func(*args , **kw)
        except tw.api.TwitterHTTPError as e:
            pass
        except error as e:
            error_count += 1
            print('URLError encoutered. Continuing.' ,
                  file=sys.stderr)  # Nuova sintassi: ("fatal error", file=sys.stderr)
            if error_count > max_errors:
                print('Too many consecutive errors... bailing out.' , file=sys.stderr)
                raise
        except BadStatusLine as e:
            error_count += 1
            print('BadStatusLine encountered. Continuing.' , file=sys.stderr)
            if error_count > max_errors:
                print('Too many consecutive errors... bailing out.' , file=sys.stderr)
                raise


def save_json(filename , data):
    with io.open('{0}.json'.format(filename) , 'w' , encoding='utf-8') as f:
        f.write(unicode(json.dumps(data , ensure_ascii=False)))
        f.close()


def read_json(filename):
    with io.open('{0}.json'.format(filename) , encoding='utf-8') as f:
        return f.read()


# FETCH_USER_TIMELINE
#
# FUNZIONE PRINCIPALE
# 
# Riceve da Skeduler_TL il since_id, il contatore del ciclo Utente, e il semaforo
# Forma la OAuth, e trasmette la OAuth e il nome dell'utente da cercare alla funzione di ricerca vera e propria
#
# FETCH_USER_TIMELINE -> harvest_user_timeline

def FETCH_USER_TIMELINE(since_id , count , i , q , semaforo , mydb):
    dev_key = config.key_list[config.indice_account_dev]

    auth = tw.oauth.OAuth(dev_key['OAUTH_TOKEN'] , dev_key['OAUTH_TOKEN_SECRET'] , dev_key['CONSUMER_KEY'] ,
                          dev_key['CONSUMER_SECRET'])

    print('********** AVVIO RICERCA {}'.format(q))
    print('********** SINCE_ID: {}'.format(since_id))

    twitter_api = tw.Twitter(
        domain='api.twitter.com' ,
        api_version='1.1' ,
        auth=auth
    )

    tweets = harvest_user_timeline(since_id , i , semaforo , twitter_api , screen_name=q , max_results=3200)

    print(str(len(tweets)))

    if len(tweets) > 0:

        # 		mydb = CONNECT_MONGODB (db, collection)

        if (config.connessione_mongodb == True):
            IMPORT_DOCS_IN_MONGO(tweets , mydb , q + "_" + count)
        else:
            save_json(q + '_' + count , tweets)

    return len(tweets)
