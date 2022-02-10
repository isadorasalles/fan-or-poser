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
	artist = items[0]

	#baixa a foto do artista com o nome que foi feita a pesquisa
	for i in artist['images']:
		if i['width'] == 640:
			urllib.request.urlretrieve(i['url'], "photos/" + artista + ".jpg")

	#pega as top_tracks dele
	uri = 'spotify:artist:' + artist['id']
	result = sp.artist_top_tracks(uri)

	#baixa 10 músicas (ou todas que podem)
	baixadas = []
	for faixa in result['tracks']:
		if len(baixadas) >= 10:
			break
		try:
			urllib.request.urlretrieve(faixa['preview_url'], "music/" + faixa['name'] + ".mp3")
			baixadas.append(faixa['name'])
		except TypeError:
			pass

	return baixadas

print(baixa('Anitta'))
