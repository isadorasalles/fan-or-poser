import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
import os


#baixa as 10 músicas mais famosas de um artista
#se não tiver disponível, retorna uma lista vazia
#pode retornar uma lista com menos de 10 músicas se menos de 10 estiverem disponíveis
def baixa(artista):
	#se conecta no servico do spotify
	sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('CLIENT_ID'),
					 client_secret=os.environ.get('CLIENT_SECRET')))
	
	#pesquisa o artista
	result = sp.search(q='artist:' + artista, type='artist')
	items = result['artists']['items']
	if len(items) == 0:
		return []

	#dos selecionados escolhe o que tem mesmo prefixo e maior popularidade
	idx = 0
	pop = 0
	for j, artist in enumerate(items):
		ok = True
		lim = min(len(artista), len(artist['name']))
		for i in range(lim):
			ok = ok and (artista[i] == artist['name'][i])
		if ok and artist['popularity'] > pop:
			idx = j
			pop = artist['popularity']
	artist = items[idx]

	if not os.path.exists("static/"):
		os.makedirs("static/")

	#baixa a foto do artista com o nome que foi feita a pesquisa
	for i in artist['images']:
		if i['width'] == 640:
			urllib.request.urlretrieve(i['url'], "static/" + artista + ".jpg")

	#pega as top_tracks dele
	uri = 'spotify:artist:' + artist['id']
	result = sp.artist_top_tracks(uri)

	if not os.path.exists("music/"):
		os.makedirs("music/")

	#baixa 10 músicas (ou todas que podem)
	baixadas = []
	for faixa in result['tracks']:
		if len(baixadas) >= 10:
			break
		try:
			urllib.request.urlretrieve(faixa['preview_url'], "music/" + faixa['name'].replace('/', ' ') + ".mp3")
			baixadas.append(faixa['name'])
		except TypeError:
			pass

	return baixadas

# print(baixa('Gilberto Gil'))
