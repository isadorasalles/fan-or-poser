import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="COLOCA_O_ID_DO_CLIENTE_AQUI",
					 client_secret="COLOCA_O_SEGREDO_DO_CLIENTE_AQUI"))

#baixa as 10 músicas mais famosas de um artista
#se não tiver disponível, retorna uma lista vazia
#pode retornar uma lista com menos de 10 músicas se menos de 10 estiverem disponíveis
def baixa(artista):
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
			urllib.request.urlretrieve(faixa['preview_url'], faixa['name'] + ".mp3")
			baixadas.append(faixa['name'])
		except TypeError:
			pass

	return baixadas

print(baixa('Anitta'))
