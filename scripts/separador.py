from spleeter.separator import Separator
import librosa         #pra ler musica
import soundfile as sf #pra salvar musica
import numpy as np
from scipy.signal import find_peaks


#determina o numero de batidas numa musica
def batidas(wav, sr):
	onset = librosa.onset.onset_strength(wav, sr = sr)
	peaks = find_peaks(onset, prominence=1)
	return len(peaks[0])


#descobre o nome da musica usando o caminho dado
def nome_musica(caminho):
	pasta = 'music/'
	extencao = '.mp3'
	return caminho[len(pasta):-len(extencao)]


#recebe uma lista de musicas e junta elas numa so
def junta_musicas(caminhos, destino):
	musicas = []
	for i in caminhos:
		wav, sr = librosa.load(i)
		musicas.append(wav)
	nova = np.zeros(len(musicas[0]))
	for i in musicas:
		nova = nova + i
	sf.write(destino, nova, sr)


#separa o vocal e retorna o arquivo sem ele
def separador_vocal(caminho):
	separator = Separator('spleeter:2stems')
	dest = 'output'
	separator.separate_to_file(caminho, dest)
	musica = nome_musica(caminho)
	return 'output/' + musica + 'accompaniment.wav'

#a ideia eh que vai passar o caminho da musica e o "nivel"
#nivel 1: nao faz nada
#nivel 2: tira vocal
#nivel 3: tira vocal e mais alguma coisa. Etc
def separador(caminho, nivel):
	pass

