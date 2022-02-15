import random
from .baixador import baixa
import pandas as pd
from .separador import separador
import logging 

def escolhe_musica(musics):
    musica_alvo = random.sample(musics, 1)
    musics.remove(musica_alvo[0])
    opcoes = list(random.sample(musics, 3))
    opcoes.extend(musica_alvo)
    opcoes = random.sample(opcoes, len(opcoes))
    ind = opcoes.index(musica_alvo[0])
    
    return musics, musica_alvo, opcoes, ind

def primeira_musica(artist):
    musicas = baixa(artist)
    if musicas != []:
        with open('static/musics.txt', 'w') as f:
            for m in musicas:
                f.write(m+'\n')
        musics, musica_alvo, opcoes, ind = escolhe_musica(musicas)
        with open('static/infos.txt', 'w') as f:
            f.write(musica_alvo[0]+';'+opcoes[0]+','+opcoes[1]+','+opcoes[2]+','+opcoes[3]+';'+str(ind)+';'+str(0)+';'+'static/'+artist+'.jpg')
        return musics, musica_alvo, opcoes, ind, 'static/'+artist+'.jpg'
    else:
        return [], [], [], -1, []

def proxima_musica():
    with open('static/infos.txt', 'r') as f:
        data = f.readlines()
    infos = data[0].split(';')
    nivel = int(infos[3]) + 1
    with open('static/musics.txt', 'r') as f:
        data = f.readlines()
    musicas = []
    for line in data:
        m = line.replace('\n', '')
        if m != infos[0]:
            musicas.append(m)
    _, musica_alvo, opcoes, ind = escolhe_musica(musicas)
    novo_alvo, _ = separador('music/'+str(musica_alvo[0])+'.mp3', nivel)
    with open('static/infos.txt', 'w') as f:
        f.write(novo_alvo+';'+opcoes[0]+','+opcoes[1]+','+opcoes[2]+','+opcoes[3]+';'+str(ind)+';'+str(nivel)+';'+infos[4])
   
    return  [novo_alvo], opcoes, ind, infos[4], nivel

def verifica_musica(i):
    with open('static/infos.txt', 'r') as f:
        data = f.readlines()
    infos = data[0].split(';')
    if int(i) == int(infos[2]):
        return True
    return False

def estado_atual():
    with open('static/infos.txt', 'r') as f:
        data = f.readlines()
    infos = data[0].split(';')
    opcoes = infos[1].replace('[', '').replace(']', '').split(',')
    return [infos[0]], opcoes, int(infos[2]), infos[3], infos[4]
