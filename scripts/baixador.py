import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request
import os


#baixa as 10 músicas mais famosas de um artista
#se não tiver disponível, retorna uma lista vazia
#pode retornar uma lista com menos de 10 músicas se menos de 10 estiverem disponíveis
def baixa(artista):
	sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('CLIENT_ID'),
					 client_secret=os.environ.get('CLIENT_SECRET')))
	result = sp.search(q='artist:' + artista, type='artist')
	items = result['artists']['items']
	if len(items) == 0:
		return []
	artista = items[0]
	uri = 'spotify:artist:' + artista['id']
	result = sp.artist_top_tracks(uri)

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

# print(baixa('Anitta'))