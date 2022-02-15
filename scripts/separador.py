from spleeter.separator import Separator
import librosa         #pra ler musica
import soundfile as sf #pra salvar musica
import numpy as np
from scipy.signal import find_peaks #pra achar o número de batidas
import os              #pra criar a pasta com as músicas
from itertools import chain, combinations #pra gerar conjunto potencia
import random

def save_music_to(original, destino):
	wav, sr = librosa.load(original)
	sf.write(destino, wav, sr)
	

#determina o numero de batidas numa musica
def batidas(caminho):
	wav, sr = librosa.load(caminho)
	onset = librosa.onset.onset_strength(wav, sr = sr)
	peaks = find_peaks(onset, prominence=1)
	return len(peaks[0])


#descobre o nome da musica usando o caminho dado
def nome_musica(caminho):
	barra = caminho.find('/')
	# extencao = caminho.find('.')
	return caminho[barra+1:-4]


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


#conjunto potencia de um iterador
def powerset(iterable):
	s = list(iterable)
	return list(chain.from_iterable(combinations(s, r)
					 for r in range(1, len(s)+1)))


#dado a escolha feito pelo escolhedor, faz uma descrição com os intrumentos
def descricao(stems, idx):
	#a tradução de cada instrumento
	traduz = {'piano' : 'piano',
			  'drums' : 'bateria',
			  'bass'  : 'baixo',
			  'other' : 'acompanhamentos*'}
	
	#gera o conjunto potencia para ver qual deles eu escolhi
	P = powerset(stems)
	P = [list(i) for i in P[:-1]]
	inst = P[idx]

	#para cada instrumento que tem, coloca a tradução dele na descrição
	s = 'Música sem vocais, '
	for i, j in enumerate(inst):
		s = s + traduz[j]
		if i != len(inst) - 1:
			s = s + ', '
	s = s + '.'
	return s


#separa usando com 5 stems
def separa_tudo(caminho):
	separator = Separator('spleeter:4stems')
	dest = 'output'
	separator.separate_to_file(caminho, dest)
	musica = nome_musica(caminho)
	return 'output/' + musica + 'accompaniment.wav'


#testa todas as combinacoes de tirar os instrumentos de uma musica
#e pega a que tem menos coisa, mas que tem coisa suficiente
def pior_possivel(musica):
	#tem que comecar separando a musica
	separa_tudo('music/' + musica + '.mp3')

	#cria os caminhos onde estao as musicas
	stems = ['drums', 'bass', 'other']
	prefixo = 'output/' + musica + '/'
	sufixo = '.wav'
	caminhos = [prefixo + i + sufixo for i in stems]

	#cria uma pasta onde vai colocar as musicas
	destino = 'temp/' + musica + '/'

	if not os.path.exists(destino):
		os.makedirs(destino)

	#pega todas as combinacoes de instrumentos
	P = powerset(caminhos)
	P = [list(i) for i in P[:-1]]

	#mede o numero de batidas da original pra comparar depois
	original = batidas('music/' + musica + '.mp3')

	#pra cada combinacao mede o numero de batidas
	num_bat = []
	for idx, s in enumerate(P):
		caminho = destino + str(idx) + '.wav'
		junta_musicas(s, caminho)
		num_batidas = batidas(caminho)
		if num_batidas*2 >= original:
			num_bat.append((num_batidas, idx))

	#coloca num vetor o numero de batidas e ordena
	num_bat = sorted(num_bat)

	#nao me julga por ter colocado num vetor nao, por favor
	#antes a ideia era outra

	#se nao tem ninguem, tem que colocar todos os instrumentos mesmo
	if len(num_bat) == 0:
		junta_musicas(caminhos, destino + str(len(P)) + '.wav')
		num_bat.append((0, len(P)))

	#retorna o destino e uma descricao
	id_escolhida = num_bat[0][1]
	return (destino + str(id_escolhida) + '.wav', descricao(stems, id_escolhida))


#separa o vocal e retorna o arquivo sem ele
def separador_vocal(caminho):
	separator = Separator('spleeter:2stems')
	dest = 'output'
	separator.separate_to_file(caminho, dest)
	musica = nome_musica(caminho)
	return 'output/' + musica + '/accompaniment.wav'


#adiciona ruído Gaussiano a musica
#quanto maior o valor da constante, menor o ruido
def adiciona_ruido(caminho, constante = 3):
	wav, sr = librosa.load(caminho)
	maxi = max(wav)
	wav = wav + np.random.normal(0, maxi/constante, len(wav))
	destino = 'temp/' + nome_musica(caminho) + '/'
	try:
		os.mkdir(destino)
	except FileExistsError:
		pass
	destino = destino + 'ruido.wav'
	sf.write(destino, wav, sr)
	return destino


#a ideia eh que vai passar o caminho da musica e o "nivel"
#nivel 0: nao faz nada
#nivel 1: tira vocal
#nivel 2: tira vocal e mais alguma coisa atrapalhando pouco
#nivel 3: adiciona ruído na música original
#nivel 4: adiciona ruído na música do nível 3
#sempre vou retornar um par ordenado (caminho, descricao)
def interface_separador(caminho, nivel):
	if nivel == 0:
		return (caminho,
				'Música original sem alterações.')
	if nivel == 1:
		return (separador_vocal(caminho),
				'Música com os vocais removidos.')
	if nivel == 2:
		return pior_possivel(nome_musica(caminho))
	if nivel == 3:
		return (adiciona_ruido(caminho),
				'Música com ruído Gaussiano adicionado.')
	if nivel == 4:
		novo_caminho, desc = pior_possivel(nome_musica(caminho))
		print('\n\n', novo_caminho, desc, '\n')
		return (adiciona_ruido(novo_caminho, 12),
				desc[:-1] + ' e com ruído Gaussiano.')

def separador(caminho, nivel):
	caminho_antigo, descricao = interface_separador(caminho, nivel)
	caminho_novo = 'music/' + nome_musica(caminho) + '_' + str(nivel) + '.wav'
	save_music_to(caminho_antigo, caminho_novo)
	return (nome_musica(caminho_novo), descricao)

print(separador('music/Dueto.mp3', 2))
