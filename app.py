from flask import Flask,render_template, Response, request, send_from_directory
import sys
# Tornado web server
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from scripts.baixador import baixa
from scripts.separador import separador
from scripts.util import primeira_musica, verifica_musica, estado_atual, proxima_musica
import os

#Debug logger
import logging 
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

musics = []

# Initialize Flask.
app = Flask(__name__)

def salva_respostas(id_):
    with open('static/acertos.txt', 'a+') as f:
        if verifica_musica(id_):
            f.write('1\n')
        else:
            f.write('0\n')

def test_options(request):
    if 'music0' in request.form:
        salva_respostas(0)
    elif 'music1' in request.form:
        salva_respostas(1)
    elif 'music2' in request.form:
        salva_respostas(2)
    elif 'music3' in request.form:
        salva_respostas(3)

def computa_pontos():
    with open('static/acertos.txt', 'r') as f:
        pontos = f.readlines()
    soma = 0
    for p in pontos:
        soma += int(p.replace('\n', ''))
    os.remove('static/acertos.txt')
    return soma

def chegou_ao_fim():
    _, _, _, nivel, _ = estado_atual()
    if nivel == '5':
        return True
    return False

#Route to render GUI
@app.route('/', methods=['POST', 'GET'])
def show_entries():
    if request.method == "POST":
        ## se o usuario marcar mais de uma resposta deve aparecer um aviso
        if len(request.form) > 1:
            musica_alvo, opcoes, ind, nivel, artista_img = estado_atual()
            return render_template('play.html', musica=musica_alvo, nivel=int(nivel), image=artista_img ,op=opcoes, i=ind, aviso=1)
        
        if 'artist' in request.form:
            musics, musica_alvo, opcoes, ind, artista_img = primeira_musica(request.form['artist'])
            logging.debug(musica_alvo)
            if musics != []:
                logging.debug(artista_img)
                return render_template('play.html', musica=musica_alvo, nivel=0, image=artista_img, op=opcoes, i=ind, aviso=0)
            else:
                return render_template('simple.html', aviso=1)

        test_options(request)
        if chegou_ao_fim():
            pontuacao = computa_pontos()
            fan = 0
            if pontuacao >= 5:
                fan = 1
            logging.debug(pontuacao)
            return render_template('score.html', pontos=pontuacao, fan=fan)
        musica_alvo, opcoes, ind, artista_img, nivel = proxima_musica()
        logging.debug(musica_alvo)
        return render_template('play.html', musica=musica_alvo, nivel=int(nivel), image=artista_img, op=opcoes, i=ind, aviso=0)
       
    return render_template('simple.html', aviso=0)

#Route to stream music
@app.route('/<string:stream_name>')
def streammp3(stream_name):
    def generate():
        try:
            song = "music/" + stream_name + ".mp3"
            with open(song, "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
        except:
            song = "music/" + stream_name + ".wav"
            with open(song, "rb") as fwav:
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)
                
    return Response(generate(), mimetype="audio/mp3")

#launch a Tornado server with HTTPServer.
if __name__ == "__main__":
    port = 5000
    http_server = HTTPServer(WSGIContainer(app))
    logging.debug("Started Server, Kindly visit http://localhost:" + str(port))
    http_server.listen(port)
    IOLoop.instance().start()
    
