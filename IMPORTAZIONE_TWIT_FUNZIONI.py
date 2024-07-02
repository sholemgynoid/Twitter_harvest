#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

def UPDATE_DATE_FIELD(tweet_list: object) -> object:
    count = 0

    print('Comincio processo di aggiornamento del campo data...')

    for tweet in tweet_list:

        count += 1

        if count % 1000 == 0:
            print('Processing tweet #{}'.format(count))

        thedate = tweet['created_at']

        proper_date = datetime.datetime.strptime(thedate , '%a %b %d %H:%M:%S +0000 %Y')

        tweet['prop_created_at'] = proper_date

    print(('Updated ' + str(count) + ' tweets.'))

    return (tweet_list)
