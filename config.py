#!/usr/bin/python
# -*- coding': utf-8 -*-

semaforo_globale = True
since_id_new = "1"
max_id_new = "1"
connessione_mongodb = False
indice_account_dev = 0

account_Gloria_Romano = {
	'CONSUMER_KEY': 'hymu28pMEQQVTURFz6HNtbeGk',
	'CONSUMER_SECRET': '9MBsaoUZzydqul0uHPRbtCqqqDMko05v5VRe9RN07rLI5mOELq',
	'OAUTH_TOKEN': '390163215-lWLli6hCtggaAlmqeZruyxlapenQSaMXMQ5Ccu53',
	'OAUTH_TOKEN_SECRET': 'Iq3akhGkmICwotk2mJiestoWTx6TqQHpUInxSOHpY6Lfz'
	}
	
account_Gaia = {
	'CONSUMER_KEY': 'bhalDifT5Gh7JeijUzaSfQ',
	'CONSUMER_SECRET': 'ltGP3YX7sGwv85TQ1eLHoGjFS6yA1OjKvtKJqwJI5M',
	'OAUTH_TOKEN': '512437392-VAvBrvMDe7t5LlrhY3hTEhN66AVQsIrjXxsqA13J',
	'OAUTH_TOKEN_SECRET': 'QzCXX28wakkYGuNaJOyWzphANXONi3cxcS6JvmtGMILoT'
	}

account_Giovanni = {
	'CONSUMER_KEY': 'xJFfmTICacWDwocDjqMsg',
	'CONSUMER_SECRET': 'd0FCC79rebwaKJVRGKwEKG7tV58aBrcAcVFwEApBt8w',
	'OAUTH_TOKEN': '50268254-ZxOTQjSmFZvb5McWpPrUUiDQvugIJxR2szlLxigJF',
	'OAUTH_TOKEN_SECRET': '0KK4y96gvqEpN1dEEURzA56pyIiu237tJTQYNIL8k'
	}

account_NFFC = {
	'CONSUMER_KEY': 'OfMk5SCZpkB1dSS8Cm9nA',
	'CONSUMER_SECRET': 'hWF8BhBU6W42cAfvufjxLgeJWTpVXFMfrGLSoutKWE',
	'OAUTH_TOKEN': '491738379-B9UALypPCzyzrWeSF3VmR5CcLpibA9NFsnuO3w6Z',
	'OAUTH_TOKEN_SECRET': 'W6yTPNIo8Eb9uxMMw7kwsToipyvOLjx22pOsiFTUc'
	}

account_Alessandra = {
	'CONSUMER_KEY': 'u9BWaMa2R5UaWlSCFPnn9g',
	'CONSUMER_SECRET': '2hgr7e6CIUDUAUNsNktssSKYrhvxd7HdBDwfFHO96A',
	'OAUTH_TOKEN': '1417616881-wE2w8dUzMHeubgpB5ELivO8c0pezlcYznRZowbp',
	'OAUTH_TOKEN_SECRET': 'hIMFnfGy52CCl5IjhcvPmrpBxFIQnaAzarcsF2o'
	}

account_Andrea = {
	'CONSUMER_KEY': '4no1zz31iilxon47e9ZgrQ',
	'CONSUMER_SECRET': 'ScFeczWHoSWTKOhlDaGMbiPTqanFbD32hZlrV8MwEg',
	'OAUTH_TOKEN': '465486573-gi0RB4CiZsQiU113vhyg9nNIRJYUVBAqoQVmSe1i',
	'OAUTH_TOKEN_SECRET': 'ocCuLk57d7Y1f0zMV4AbQ36D1HjHHzoILJW1EwJBU'
	}
	
account_Mirella = {
	'CONSUMER_KEY': 'fewS1v95vzS7t4xEBw6yImOSk',
	'CONSUMER_SECRET': 'VjLuUImHmNPhIvByiEPtRFBlGlI1MaxhFK6fe8z4DmCekAo2cs',
	'OAUTH_TOKEN': '844509985954521089-9d3JGbZRkvCxp0E0voIzhXRUVpuai63',
	'OAUTH_TOKEN_SECRET': 'LmdFc3VdMVVYXTW6behEOSQzSz5hIWOCmHU5cah39ow81'
	}

account_Monia = {
	'CONSUMER_KEY': 'P9pnC6q75BXfdxQpspgtzHnqe',
	'CONSUMER_SECRET': 'IQMv7HV9OvM92PBVj3xmxqLTPGSUe5SImVPSPxxbOc7yNAZpwt',
	'OAUTH_TOKEN': '790535575782748161-XvSzjrg6fpjgR1DVTKfe7h5LjScADqb',
	'OAUTH_TOKEN_SECRET': '4zBsNnKfKBEl77WwKLSuuPAUOgUkSeP7R09mj10BfX7az'
	}

account_Vittorio = {
	'CONSUMER_KEY': 'Pamn0ueC69u03fkdycusA',
	'CONSUMER_SECRET': 'ItyZn827YfKLZVP4V3wYlnyTa7jeAJX67PJ6k8mgW8',
	'OAUTH_TOKEN': '138054290-bOt6Pc5jwbQ35E5naH3HOq1Q8Xq7ubpXUBzJGSDy',
	'OAUTH_TOKEN_SECRET': '3Qxa6VpBesPs6PHHvyNulD7ggn49AvmdXbbC3OI'
	}

key_list = [account_Gloria_Romano,  #0
	account_Gaia,					#1
	account_Giovanni,				#2
	account_NFFC,					#3
	account_Alessandra,				#4
	account_Andrea,					#5
	account_Mirella,				#6
	account_Monia,					#7
	account_Vittorio				#8
	]