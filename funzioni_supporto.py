def compila_array_progressivo (array_da_ordinare, valore_aggiuntivo):
	
	lunghezza_array = len (array_da_ordinare)
	array_ordinato = []
	array_ordinato.insert (0, valore_aggiuntivo)
	
	for i in range (lunghezza_array-1):
		array_ordinato.insert (i+1, array_da_ordinare[i])
		
	return array_ordinato
	
def media_array (array):
	
	average = sum (array) / len (array)
	
	return average